"""Behavioral checks for the candidate scanner; run with python3 -B this_file.py."""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch


SCANNER = Path(__file__).with_name("smell-scan.py")


class ScannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="test-forge-scan-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def source(self, code, name="test_example.py"):
        path = self.root / name
        path.write_text(textwrap.dedent(code), encoding="utf-8")
        return path

    def run_scan(self, *paths):
        return subprocess.run(
            [sys.executable, "-B", str(SCANNER), *map(str, paths)],
            capture_output=True, text=True, timeout=10,
        )

    def assert_clean(self, code):
        result = self.run_scan(self.source(code))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("candidate(s)", result.stdout, result.stdout)
        return result

    def test_both_branches_assert(self):
        self.assert_clean("""
            def test_paths(x):
                if x:
                    assert x == 1
                else:
                    assert x == 0
        """)

    def test_tight_interval_is_not_an_unfalsifiable_range(self):
        self.assert_clean("def test_probability(p):\n    assert 0.49 < p < 0.51\n")

    def test_mock_routing_is_not_a_return_value_oracle(self):
        self.assert_clean("""
            def test_routes():
                callback = MagicMock(return_value=3)
                dispatch(callback)
                callback.assert_called_once()
        """)

    def test_repeated_calls_can_observe_different_states(self):
        self.assert_clean("def test_progress():\n    assert next_value() != next_value()\n")

    def test_repeated_equal_calls_can_test_repeatability(self):
        self.assert_clean("def test_repeatability():\n    assert sample() == sample()\n")

    def test_exact_cardinality_is_not_liveness(self):
        self.assert_clean("def test_correct_single_result(items):\n    assert len(items) == 1\n")

    def test_membership_and_domain_tolerances_need_semantics(self):
        self.assert_clean("""
            def test_choice(value):
                assert value in allowed
            def test_distance(actual, expected):
                assert abs(actual - expected) < 20
        """)

    def test_one_sided_guard_is_a_candidate(self):
        result = self.run_scan(self.source("""
            def test_converges(model):
                if model.ready:
                    assert model.error < 0.01
        """))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2-conditional-guard", result.stdout)

    def test_unconditional_assertion_prevents_guard_candidate(self):
        self.assert_clean("""
            def test_paths(x):
                assert x is not None
                if x:
                    assert x == 1
        """)

    def test_same_name_equality_is_a_candidate(self):
        result = self.run_scan(self.source("def test_value(x):\n    assert x == x\n"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("3-same-operand", result.stdout)

    def test_equality_method_is_a_candidate(self):
        result = self.run_scan(self.source("def test_value(x):\n    np.testing.assert_allclose(x, x)\n"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("3-same-operand", result.stdout)

    def test_nan_inequality_is_not_same_operand_equality(self):
        self.assert_clean("def test_nan(x):\n    assert x != x\n")

    def test_correctness_name_with_liveness_is_a_candidate(self):
        result = self.run_scan(self.source("def test_accurate(model):\n    assert model() is not None\n"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("7-oracle-name-on-smoke", result.stdout)

    def test_marker_does_not_certify_a_liveness_assertion(self):
        result = self.run_scan(self.source("@pytest.mark.contract\ndef test_accurate(model):\n    assert len(model()) > 0\n"))
        self.assertIn("7-oracle-name-on-smoke", result.stdout)

    def test_oracle_marker_can_seed_a_candidate(self):
        result = self.run_scan(self.source("@pytest.mark.oracle\ndef test_result(model):\n    assert model() is not None\n"))
        self.assertIn("7-oracle-name-on-smoke", result.stdout)

    def test_nested_helpers_are_not_independent_tests(self):
        result = self.assert_clean("""
            def test_outer():
                def test_inner(x):
                    assert x == x
                assert external() == expected
        """)
        self.assertIn("tests=1", result.stdout)

    def test_async_and_class_tests_are_inspected(self):
        result = self.assert_clean("""
            async def test_async():
                assert await value() == expected
            class Checks:
                def test_method(self):
                    self.assertEqual(actual, expected)
        """)
        self.assertIn("tests=2", result.stdout)

    def test_syntax_failure_is_incomplete_inspection(self):
        result = self.run_scan(self.source("def test_broken(:"))
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("parsed=0", result.stdout)
        self.assertIn("errors=1", result.stdout)
        self.assertNotIn("no mechanical smell", result.stdout)

    def test_partial_parse_failure_preserves_successful_findings(self):
        self.source("def test_value(x):\n    assert x == x\n")
        self.source("def test_broken(:", "broken.py")
        result = self.run_scan(self.root)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("parsed=1", result.stdout)
        self.assertIn("errors=1", result.stdout)
        self.assertIn("3-same-operand", result.stdout)

    def test_invalid_target_among_valid_targets_is_an_error(self):
        valid = self.source("def test_value():\n    assert actual == expected\n")
        result = self.run_scan(valid, self.root / "missing")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("parsed=1", result.stdout)

    def test_decode_failure_is_an_error(self):
        path = self.root / "test_bad.py"
        path.write_bytes(b"\xff\xfe")
        result = self.run_scan(path)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("errors=1", result.stdout)

    def test_deep_fixture_expression_does_not_abort_a_batch(self):
        # Valid generated fixture: deeper than NodeVisitor's recursive descent,
        # but irrelevant to finding the test definitions that follow it.
        code = "VALUES = " + " + ".join(["[1]"] * 800)
        code += "\ndef test_deep(x):\n    assert x == x\n"
        compile(code, "deep.py", "exec")
        self.source(code, "b_deep.py")
        self.source("def test_first(x):\n    assert x == x\n", "a_first.py")
        result = self.run_scan(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("discovered=2 parsed=2 tests=2 candidates=2 errors=0", result.stdout)
        self.assertIn("test_deep", result.stdout)
        self.assertIn("test_first", result.stdout)

    def test_python_source_encodings_are_inspected(self):
        fixtures = {
            "bom.py": b"\xef\xbb\xbfdef test_value(x):\n    assert x == x\n",
            "latin1.py": b'# coding: latin-1\nLABEL = "caf\xe9"\ndef test_value(x):\n    assert x == x\n',
        }
        for name, content in fixtures.items():
            with self.subTest(name=name):
                compile(content, name, "exec")
                path = self.root / name
                path.write_bytes(content)
                result = self.run_scan(path)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("parsed=1 tests=1 candidates=1 errors=0", result.stdout)
                self.assertIn("3-same-operand", result.stdout)

    def test_invalid_encoding_declarations_remain_errors(self):
        fixtures = {
            "unknown.py": b"# coding: unavailable_codec\ndef test_value():\n    assert True\n",
            "conflict.py": b"\xef\xbb\xbf# coding: latin-1\ndef test_value():\n    assert True\n",
        }
        for name, content in fixtures.items():
            with self.subTest(name=name):
                with self.assertRaises(SyntaxError):
                    compile(content, name, "exec")
                path = self.root / name
                path.write_bytes(content)
                result = self.run_scan(path)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("parsed=0 tests=0 candidates=0 errors=1", result.stdout)

    def test_definitions_under_statement_containers_are_inspected(self):
        path = self.source("""
            if enabled:
                def test_if(): pass
            else:
                async def test_else(): pass
            try:
                def test_try(): pass
            except Exception:
                def test_except(): pass
            else:
                def test_try_else(): pass
            finally:
                def test_finally(): pass
            with context():
                class Cases:
                    def test_method(self): pass
            for item in items:
                def test_loop(): pass
            def factory():
                class Hidden:
                    def test_not_module_level(self): pass
        """)
        result = self.run_scan(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("tests=8 candidates=0 errors=0", result.stdout)

    def test_assertions_under_statement_containers_are_inspected(self):
        result = self.run_scan(self.source("""
            def test_containers(x):
                try:
                    assert x == x
                except Exception:
                    assert x == x
                else:
                    assert x == x
                finally:
                    assert x == x
                with context():
                    assert x == x
                for item in items:
                    assert x == x
        """))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("tests=1 candidates=6 errors=0", result.stdout)

    def test_match_cases_follow_the_running_interpreters_grammar(self):
        result = self.run_scan(self.source("""
            match value:
                case 1:
                    def test_match(x):
                        match x:
                            case 1:
                                assert x == x
        """))
        if hasattr(ast, "Match"):
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("parsed=1 tests=1 candidates=1 errors=0", result.stdout)
        else:
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("parsed=0 tests=0 candidates=0 errors=1", result.stdout)

    def test_inspection_failure_preserves_completed_tests_and_later_files(self):
        module = self.load_scanner()
        self.source("""
            def test_completed(x):
                assert x == x
            def test_interrupted(x):
                assert x == x
        """, "a_partial.py")
        self.source("def test_later(x):\n    assert x == x\n", "b_later.py")
        original = module.claims_strong

        def interrupted(node):
            if node.name == "test_interrupted":
                raise RecursionError("inspection exhausted")
            return original(node)

        with patch.object(module, "claims_strong", side_effect=interrupted):
            with patch.object(sys, "argv", [str(SCANNER), str(self.root)]):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    status = module.main()
        self.assertEqual(status, 2)
        self.assertIn("discovered=2 parsed=2 tests=2 candidates=2 errors=1", out.getvalue())
        self.assertIn("test_completed", out.getvalue())
        self.assertIn("test_later", out.getvalue())
        self.assertNotIn("test_interrupted", out.getvalue())
        self.assertIn("a_partial.py", err.getvalue())
        self.assertIn("RecursionError: inspection exhausted", err.getvalue())

    def test_duplicate_targets_are_counted_once(self):
        path = self.source("def test_value():\n    assert actual == expected\n")
        result = self.run_scan(path, self.root, path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("discovered=1 parsed=1 tests=1", result.stdout)

    def test_no_named_tests_is_not_a_completed_test_inspection(self):
        result = self.run_scan(self.source("def helper():\n    return 1\n"))
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("tests=0", result.stdout)

    def test_empty_directory_is_an_error(self):
        self.assertEqual(self.run_scan(self.root).returncode, 2)

    def test_extension_option_still_parses_python(self):
        self.source("def test_value():\n    assert actual == expected\n", "case.txt")
        result = self.run_scan(self.root, "--ext", ".txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("parsed=1", result.stdout)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "requires filesystem FIFO support")
    def test_directory_special_file_cannot_block_inspection(self):
        os.mkfifo(self.root / "waiting.py")
        result = self.run_scan(self.root)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("not a regular file", result.stderr)

    def load_scanner(self):
        spec = importlib.util.spec_from_file_location("test_forge_scan", SCANNER)
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {spec.name: module}):
            spec.loader.exec_module(module)
        return module

    def test_read_error_is_not_a_clean_scan(self):
        module = self.load_scanner()
        path = self.source("def test_value():\n    assert actual == expected\n")
        with patch.object(module.tokenize, "open", side_effect=PermissionError("read denied")):
            with patch.object(sys, "argv", [str(SCANNER), str(path)]):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(module.main(), 2)

    def test_traversal_error_is_not_silently_ignored(self):
        module = self.load_scanner()

        def denied_walk(path, *, onerror, followlinks):
            onerror(PermissionError("walk denied"))
            return iter(())

        with patch("os.walk", side_effect=denied_walk):
            with patch.object(sys, "argv", [str(SCANNER), str(self.root)]):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    self.assertEqual(module.main(), 2)
                self.assertIn("walk denied", err.getvalue())


if __name__ == "__main__":
    unittest.main()
