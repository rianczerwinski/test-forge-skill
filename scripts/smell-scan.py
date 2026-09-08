#!/usr/bin/env python3
"""Seed Python test review with syntax candidates, never an assurance verdict.

Usage: python3 smell-scan.py <file-or-directory> [...] [--ext .py]
Directories use the suffix filter; explicit files are always parsed as Python.
Directory symlinks are not traversed; explicitly supplied symlink roots are read.
Named test functions/methods are inspected without executing imports or tests.
Nested helper functions are excluded. This is not test-runner collection.

Detectors: one-sided conditional assertions; same-name equality operands;
strong names/oracle markers accompanied only by recognized liveness assertions.
Assertions include assert statements and standalone assert*-named calls.
Control flow, custom equality, indirect assertions, oracle provenance, numeric
tolerances, mock dataflow, seams, runner selection, and redundancy need review.

Exit 0: inspection completed, with or without candidates. Exit 2: incomplete
inspection (including partial errors) or no named tests. Counts describe only
the supplied Python population; candidate absence is not evidence of test quality.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass, field
import os
from pathlib import Path
import stat
import sys


STRONG_NAME_WORDS = (
    "accura", "correct", "matches", "recover", "localiz", "separat", "equival",
    "converg", "exact", "precise", "identif",
)
EQ_ASSERTS = {
    "assert_allclose", "assert_array_equal", "assert_array_almost_equal",
    "assert_almost_equal", "assert_equal", "assertEqual", "assertAlmostEqual",
}
FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef)


def callee(call):
    return getattr(call.func, "attr", getattr(call.func, "id", ""))


def named_tests(tree):
    """Visit module/class/control-flow definitions, but never function interiors."""
    found = []

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            if node.name.startswith("test"):
                found.append(node)

        visit_AsyncFunctionDef = visit_FunctionDef

    Visitor().visit(tree)
    return found


def assertions(body, guarded=False):
    for stmt in body:
        if isinstance(stmt, ast.Assert):
            yield stmt.test, stmt.lineno, guarded
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            if callee(stmt.value).startswith("assert"):
                yield stmt.value, stmt.lineno, guarded
        if isinstance(stmt, (*FUNCTIONS, ast.ClassDef)):
            continue
        # A complete if/else is not itself evidence of an assertion-free path.
        guard = guarded or (isinstance(stmt, ast.If) and not stmt.orelse)
        for field_name in ("body", "orelse", "finalbody"):
            yield from assertions(getattr(stmt, field_name, []), guard)
        for handler in getattr(stmt, "handlers", []):
            yield from assertions(handler.body, guard)
        for case in getattr(stmt, "cases", []):
            yield from assertions(case.body, guard)


def same_operand(expr):
    if isinstance(expr, ast.Compare) and len(expr.ops) == 1 and isinstance(expr.ops[0], ast.Eq):
        left, right = expr.left, expr.comparators[0]
    elif isinstance(expr, ast.Call) and callee(expr) in EQ_ASSERTS and len(expr.args) >= 2:
        left, right = expr.args[:2]
    else:
        return False
    # Repeated calls, properties and indexing may produce different values.
    return isinstance(left, ast.Name) and isinstance(right, ast.Name) and left.id == right.id


def liveness(expr):
    if isinstance(expr, ast.Call):
        return callee(expr) == "assertIsNotNone"
    if not isinstance(expr, ast.Compare) or len(expr.ops) != 1:
        return False
    left, op, right = expr.left, expr.ops[0], expr.comparators[0]
    if isinstance(op, ast.IsNot) and isinstance(right, ast.Constant) and right.value is None:
        return True
    if not (isinstance(left, ast.Call) and callee(left) == "len" and isinstance(right, ast.Constant)):
        return False
    return ((isinstance(op, (ast.Gt, ast.NotEq)) and right.value == 0)
            or (isinstance(op, ast.GtE) and right.value == 1))


def claims_strong(node):
    words = any(word in node.name.lower() for word in STRONG_NAME_WORDS)
    oracle_marker = any(
        isinstance(part, ast.Attribute) and part.attr == "oracle"
        for decorator in node.decorator_list for part in ast.walk(decorator)
    )
    return words or oracle_marker


@dataclass
class ScanResult:
    tests: int = 0
    findings: list[tuple[int, str, str, str]] = field(default_factory=list)
    error: str | None = None


def scan_file(path):
    result = ScanResult()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError) as err:
        result.error = f"{path}: {err}"
        return result
    for node in named_tests(tree):
        result.tests += 1
        units = list(assertions(node.body))
        if not units:
            continue

        def add(line, detector, evidence):
            result.findings.append((line, detector, node.name, evidence))

        if all(guarded for _, _, guarded in units):
            add(node.lineno, "2-conditional-guard",
                "recognized assertions occur under one-sided guards; inspect possible no-assertion paths")
        for expr, line, _ in units:
            if same_operand(expr):
                add(line, "3-same-operand", "same-name equality operands; inspect independence and equality semantics")
        if claims_strong(node) and all(liveness(expr) for expr, _, _ in units):
            add(node.lineno, "7-oracle-name-on-smoke",
                "strong name/oracle marker with only recognized liveness checks; inspect the claimed behavior")
    return result


def gather_files(paths, ext):
    files, errors = set(), []

    def add_file(path):
        try:
            if not stat.S_ISREG(path.stat().st_mode):
                errors.append(f"{path}: not a regular file")
                return
            files.add(path.resolve())
        except (OSError, RuntimeError) as err:
            errors.append(f"{path}: {err}")

    for path in paths:
        try:
            mode = path.stat().st_mode
            if stat.S_ISDIR(mode):
                def onerror(err):
                    errors.append(f"{path}: {err}")

                for directory, dirs, names in os.walk(path, onerror=onerror, followlinks=False):
                    dirs.sort()
                    for name in sorted(names):
                        if name.endswith(ext):
                            add_file(Path(directory) / name)
            elif stat.S_ISREG(mode):
                add_file(path)
            else:
                errors.append(f"{path}: neither a regular file nor directory")
        except (OSError, RuntimeError) as err:
            errors.append(f"{path}: {err}")
    return sorted(files), errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--ext", default=".py", help="directory suffix filter; all inputs use Python syntax")
    args = parser.parse_args()
    files, errors = gather_files(args.paths, args.ext)
    parsed = inspected = 0
    findings = []
    for path in files:
        result = scan_file(path)
        if result.error is not None:
            errors.append(result.error)
            continue
        parsed += 1
        inspected += result.tests
        findings.extend((path, *finding) for finding in result.findings)
    print(f"discovered={len(files)} parsed={parsed} tests={inspected} candidates={len(findings)} errors={len(errors)}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if findings:
        print(f"{len(findings)} candidate(s); confirm each against the actual claim:")
        for path, line, detector, name, evidence in findings:
            print(f"{path}:{line} [{detector}] {name} — {evidence}")
    if errors or inspected == 0:
        print("incomplete inspection" if errors else "no inspectable named tests", file=sys.stderr)
        return 2
    if not findings:
        print("no mechanical smell candidates in the inspected test functions")
    print("Candidate absence is not assurance; semantics, provenance, seams and runner selection require review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
