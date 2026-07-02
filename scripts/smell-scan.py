#!/usr/bin/env python3
"""Seed a test-suite audit with category-collapse candidates — AST-based, context-aware.

Heuristic, not a judge: every hit is a *candidate* a human (or an audit agent) must
confirm. But unlike a line-regex scanner, this reads each test function's structure,
so it can apply the one rule that separates a smell from a legitimate test:

    A weak assertion (liveness / range / membership / mock-called) is a SMELL only
    when it is the test's SOLE signal, or when the test NAME/marker claims a stronger
    kind than the assertion delivers. The same assertion inside a @pytest.mark.contract
    test, or alongside a real assertion, is legitimate — and is NOT flagged.

That context-sensitivity is why this is an AST pass, not a grep: it needs per-function
assertion scope and the test's declared kind. Regex flags `assert 0<=p<=1` everywhere;
this flags it only when it stands alone in a test that isn't declared a contract.

An "assertion" here is both the `assert` keyword AND the assertion-method idioms real
suites use — `np.testing.assert_allclose`, `self.assertEqual`, `mock.assert_called_once`
— detected as any call whose name/attribute starts with "assert". Missing these would
blind the scanner to most numpy/unittest tests.

Detectors (map to references/audit.md §"The seven category-collapse detectors"):
  2  conditional-guard can't-fail  — ALL assertions nested in an `if` (scope-aware:
                                     catches guards whose body also has setup/loops)
  3  in-test tautology             — assert X <op> X, or assert_allclose(x, x)
  4  weakened-until-unfalsifiable  — sole/so-claimed weak assert: full-range bound,
                                     membership, or loose tolerance (atol/rtol/abs()<N)
  5  mock-shadow                   — asserted value traces to a MagicMock(return_value),
                                     or `.assert_called*` is the SOLE signal
  7  oracle-name-on-smoke          — strong-claim name, but every assertion is liveness

Not mechanically detectable (still a human/agent read): circular goldens (needs to know
how the golden was generated) and episode-file redundancy (needs cross-file semantics).

Usage:
    smell-scan.py <path> [<path> ...]        # files and/or dirs; dirs scanned recursively
    smell-scan.py tests/ --ext .py

Language note: AST parsing is Python-only. The detector *concepts* are language-agnostic;
for jest/go/rust, port the classifier — but the scope-aware structure is the point.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

# A test name whose word claims a stronger kind than a liveness assert can deliver.
STRONG_NAME_WORDS = (
    "accura", "correct", "matches", "recover", "localiz", "separat", "equival",
    "converg", "exact", "precise", "identif",
)
# Markers that DECLARE a kind. A weak assertion under an explicit contract/property/
# smoke marker is legitimate for that kind and must not be flagged as a collapse.
KIND_MARKERS = {"oracle", "property", "regression", "contract", "smoke"}
# Approximate-equality assertion methods that carry a tolerance kwarg.
TOL_ASSERTS = {"assert_allclose", "assert_array_almost_equal", "assert_almost_equal", "assertAlmostEqual"}
# Equality assertion methods whose first two args, if identical, form a tautology.
EQ_ASSERTS = {"assert_allclose", "assert_array_equal", "assert_array_almost_equal",
              "assert_almost_equal", "assert_equal", "assertEqual", "assertAlmostEqual"}
# atol/rtol at or above this is "wide" for O(1)–O(10) DSP/embedding quantities. Domain
# dependent — hence candidate-only, and only when the test isn't a declared weak kind.
WIDE_TOL = 1.0
# abs(a-b) < N with N at or above this is a loose absolute tolerance for the same reason.
WIDE_ABS = 10.0


def _callee_name(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return ""


def _is_assert_call(node: ast.expr) -> bool:
    # np.testing.assert_allclose(...), self.assertEqual(...), mock.assert_called_once()
    return isinstance(node, ast.Call) and _callee_name(node).startswith("assert")


class Unit:
    """One assertion: either an `assert` statement or an assertion-method call."""
    __slots__ = ("node", "lineno", "in_guard", "is_kw")

    def __init__(self, node, lineno, in_guard, is_kw):
        self.node = node          # ast.Assert  (is_kw) or ast.Call
        self.lineno = lineno
        self.in_guard = in_guard
        self.is_kw = is_kw

    @property
    def test(self):
        return self.node.test if self.is_kw else self.node


def _is_none_check(t: ast.expr) -> bool:
    return isinstance(t, ast.Compare) and any(
        isinstance(op, (ast.Is, ast.IsNot)) and isinstance(c, ast.Constant) and c.value is None
        for op, c in zip(t.ops, t.comparators)
    )


def _is_len_liveness(t: ast.expr) -> bool:
    if not (isinstance(t, ast.Compare) and len(t.ops) == 1):
        return False
    left, right = t.left, t.comparators[0]
    if not (isinstance(left, ast.Call) and isinstance(left.func, ast.Name) and left.func.id == "len"):
        return False
    return isinstance(right, ast.Constant) and right.value in (0, 1)


def _is_full_range(t: ast.expr) -> bool:
    if not (isinstance(t, ast.Compare) and len(t.ops) == 2):
        return False
    lo, hi = t.left, t.comparators[1]
    return (
        all(isinstance(op, (ast.Lt, ast.LtE)) for op in t.ops)
        and isinstance(lo, ast.Constant) and isinstance(lo.value, (int, float))
        and isinstance(hi, ast.Constant) and isinstance(hi.value, (int, float))
    )


def _is_membership(t: ast.expr) -> bool:
    return isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(t.ops[0], ast.In)


def _is_wide_abs_tol(t: ast.expr) -> bool:
    if not (isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(t.ops[0], (ast.Lt, ast.LtE))):
        return False
    left, right = t.left, t.comparators[0]
    if not (isinstance(left, ast.Call) and isinstance(left.func, ast.Name) and left.func.id == "abs"):
        return False
    return isinstance(right, ast.Constant) and isinstance(right.value, (int, float)) and abs(right.value) >= WIDE_ABS


def unit_liveness(u: Unit) -> bool:
    if u.is_kw:
        return _is_none_check(u.test) or _is_len_liveness(u.test)
    return _callee_name(u.node) in ("assertIsNotNone", "assertIsNone")


def unit_mock_called(u: Unit) -> bool:
    if u.is_kw:
        return any(isinstance(s, ast.Attribute) and (s.attr.startswith("assert_called")
                   or s.attr in ("called", "call_count")) for s in ast.walk(u.test))
    return _callee_name(u.node).startswith("assert_called")


def unit_tautology(u: Unit):
    if u.is_kw:
        t = u.test
        if isinstance(t, ast.Compare) and len(t.ops) == 1 and ast.dump(t.left) == ast.dump(t.comparators[0]):
            return True
        return False
    if _callee_name(u.node) in EQ_ASSERTS and len(u.node.args) >= 2:
        return ast.dump(u.node.args[0]) == ast.dump(u.node.args[1])
    return False


def unit_wide_tol(u: Unit) -> bool:
    if u.is_kw:
        return _is_wide_abs_tol(u.test)
    if _callee_name(u.node) in TOL_ASSERTS:
        for kw in u.node.keywords:
            if kw.arg in ("atol", "rtol") and isinstance(kw.value, ast.Constant) \
                    and isinstance(kw.value.value, (int, float)) and kw.value.value >= WIDE_TOL:
                return True
    return False


class _Fn:
    def __init__(self, node: ast.FunctionDef):
        self.name = node.name
        self.markers = self._markers(node)
        self.units: list[Unit] = []
        for stmt, in_guard in self._walk(node.body, False):
            if isinstance(stmt, ast.Assert):
                self.units.append(Unit(stmt, stmt.lineno, in_guard, True))
            elif isinstance(stmt, ast.Expr) and _is_assert_call(stmt.value):
                self.units.append(Unit(stmt.value, stmt.lineno, in_guard, False))

    @staticmethod
    def _markers(node: ast.FunctionDef) -> set[str]:
        out: set[str] = set()
        for d in node.decorator_list:
            for sub in ast.walk(d):
                if isinstance(sub, ast.Attribute) and sub.attr in KIND_MARKERS:
                    out.add(sub.attr)
        return out

    def _walk(self, body, in_guard):
        # Yield every statement with whether it sits under an `if` (any depth). An `if`
        # guards both its body and its else; loops/with/try preserve the inherited state.
        for stmt in body:
            yield stmt, in_guard
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue  # don't descend into nested defs
            guard = in_guard or isinstance(stmt, ast.If)
            for field in ("body", "orelse", "finalbody"):
                sub = getattr(stmt, field, None)
                if sub:
                    yield from self._walk(sub, guard)
            for handler in getattr(stmt, "handlers", []):
                yield from self._walk(handler.body, guard)

    def claims_strong(self) -> bool:
        if "oracle" in self.markers:
            return True
        low = self.name.lower()
        return any(w in low for w in STRONG_NAME_WORDS)

    def declares_weak_kind(self) -> bool:
        return bool(self.markers & {"contract", "property", "smoke", "regression"})


def scan_file(path: Path):
    findings = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError) as err:
        print(f"warn: skip {path}: {err}", file=sys.stderr)
        return findings

    def add(lineno, detector, name, evidence):
        findings.append((f"{path}:{lineno}", detector, name, evidence))

    for node in ast.walk(tree):
        if not (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test")):
            continue
        fn = _Fn(node)
        if not fn.units:
            continue

        # 2 — conditional-guard can't-fail: every assertion is inside an `if`.
        if all(u.in_guard for u in fn.units):
            add(node.lineno, "2-conditional-guard", fn.name,
                "all assertions nested in an if — the non-precondition path runs zero asserts")

        # 3 — tautology (any unit)
        for u in fn.units:
            if unit_tautology(u):
                add(u.lineno, "3-tautology", fn.name, "assertion compares a value to itself")

        # 7 — oracle-name-on-smoke: strong name/marker, every assertion liveness-only
        if fn.claims_strong() and all(unit_liveness(u) for u in fn.units):
            add(node.lineno, "7-oracle-name-on-smoke", fn.name,
                "name/marker claims correctness; every assertion is liveness (not-None / len)")

        # 4 & 5 — weak SOLE assertion, gated by declared kind (this kills the FP wave)
        if len(fn.units) == 1 and not fn.declares_weak_kind():
            u = fn.units[0]
            if u.is_kw and _is_full_range(u.test):
                why = "claims accuracy" if fn.claims_strong() else "the sole assertion"
                add(u.lineno, "4-unfalsifiable-range", fn.name,
                    f"full-range bound is {why} — cannot fail on correctness")
            elif u.is_kw and _is_membership(u.test):
                add(u.lineno, "4-membership", fn.name, "membership is the sole assertion — N-of-M, weak")
            # NB: a sole `mock.assert_called_once()` is routing verification = a legitimate
            # (if thin) contract, NOT mock-shadow. The real shadow is asserting the mock's
            # configured RETURN value, caught by 5-mock-shadow-return below. If such a
            # contract test under-covers a numeric module, kind-coverage.py flags it, not this.

        # 4 — loose tolerance (abs()<N or assert_allclose atol/rtol), outside weak kinds
        if not fn.declares_weak_kind():
            for u in fn.units:
                if unit_wide_tol(u):
                    add(u.lineno, "4-loose-tolerance", fn.name,
                        "tolerance (abs()<N or atol/rtol) likely far above the noise floor — confirm vs scale")

        # 5 — mock-shadow proper: an assertion references a MagicMock(return_value=...)
        mock_names = set()
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                callee = getattr(stmt.value.func, "id", getattr(stmt.value.func, "attr", ""))
                if callee in ("MagicMock", "Mock") and any(k.arg == "return_value" for k in stmt.value.keywords):
                    mock_names.update(t.id for t in stmt.targets if isinstance(t, ast.Name))
        if mock_names and any(
            isinstance(s, ast.Name) and s.id in mock_names
            for u in fn.units for s in ast.walk(u.test)
        ):
            add(node.lineno, "5-mock-shadow-return", fn.name,
                f"assertion references MagicMock(return_value=...) ({', '.join(sorted(mock_names))}) — may check the configured return")

    return findings


def gather_files(paths, ext):
    files = []
    for p in paths:
        if p.is_dir():
            files.extend(sorted(p.rglob(f"*{ext}")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"warn: {p} is neither file nor dir", file=sys.stderr)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="AST-based, context-aware test-smell candidate scanner.")
    ap.add_argument("paths", nargs="+", type=Path, help="test files and/or directories")
    ap.add_argument("--ext", default=".py")
    args = ap.parse_args()

    files = gather_files(args.paths, args.ext)
    if not files:
        # Loud failure, not a false all-clear: pointing at an empty/wrong path must error.
        print(f"error: no *{args.ext} files found under {', '.join(map(str, args.paths))}", file=sys.stderr)
        return 2

    grouped: dict[str, list[str]] = {}
    for path in files:
        for loc, detector, name, evidence in scan_file(path):
            grouped.setdefault(detector, []).append(f"{loc}  {name} — {evidence}")

    if not grouped:
        print(f"no mechanical smell candidates across {len(files)} file(s). "
              "Circular goldens and episode-file redundancy still need a human/agent read.")
        return 0

    total = sum(len(v) for v in grouped.values())
    print(f"# {total} candidate(s) across {len(files)} file(s) — CONFIRM each; heuristics over-flag.\n")
    for detector in sorted(grouped):
        print(f"## {detector}  ({len(grouped[detector])})")
        for entry in grouped[detector]:
            print(f"  {entry}")
        print()
    print("Not detected mechanically (need a human/agent read): circular goldens, episode-file redundancy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
