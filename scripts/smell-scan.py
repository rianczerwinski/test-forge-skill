#!/usr/bin/env python3
"""Seed Python test review with syntax candidates, never an assurance verdict.

Usage: python3 smell-scan.py <file-or-directory> [...] [--ext .py]
Directories use the suffix filter; explicit files are always parsed as Python.
Directory symlinks are not traversed; explicitly supplied symlink roots are read.
Named test functions/methods are inspected without executing imports or tests.
Nested helper functions are excluded. This is not test-runner collection.
Python encoding declarations and UTF-8 byte-order marks are honored.

Detectors: one-sided conditional assertions; same-name equality operands;
strong names/oracle markers accompanied only by recognized liveness assertions.
Assertions include assert statements and standalone assert*-named calls.
Control flow, custom equality, indirect assertions, oracle provenance, numeric
tolerances, mock dataflow, seams, runner selection, and redundancy need review.

Exit 0: inspection completed, with or without candidates. Exit 2: incomplete
inspection (including partial errors) or no named tests. Counts describe only
the supplied Python population; candidate absence is not evidence of test quality.
Parsed files and fully inspected tests are counted separately; completed tests'
findings survive a later inspection failure in the same file or batch.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass, field
import os
from pathlib import Path
import stat
import sys
import tokenize


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


def child_statements(node):
    """Only statement containers can hold definitions or standalone assertions."""
    yield from getattr(node, "body", ())
    for handler in getattr(node, "handlers", ()):
        yield from handler.body
    for field_name in ("orelse", "finalbody"):
        yield from getattr(node, field_name, ())
    for case in getattr(node, "cases", ()):
        yield from case.body


def named_tests(tree):
    """Iterative source-order walk; skip expressions and function interiors."""
    pending = list(reversed(list(child_statements(tree))))
    while pending:
        node = pending.pop()
        if isinstance(node, FUNCTIONS):
            if node.name.startswith("test"):
                yield node
        else:
            pending.extend(reversed(list(child_statements(node))))


def assertions(body, guarded=False):
    pending = [(stmt, guarded) for stmt in reversed(body)]
    while pending:
        stmt, guarded = pending.pop()
        if isinstance(stmt, ast.Assert):
            yield stmt.test, stmt.lineno, guarded
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            if callee(stmt.value).startswith("assert"):
                yield stmt.value, stmt.lineno, guarded
        if isinstance(stmt, (*FUNCTIONS, ast.ClassDef)):
            continue
        # A complete if/else is not itself evidence of an assertion-free path.
        guard = guarded or (isinstance(stmt, ast.If) and not stmt.orelse)
        pending.extend((child, guard) for child in reversed(list(child_statements(stmt))))


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
    parsed: bool = False
    tests: int = 0
    findings: list[tuple[int, str, str, str]] = field(default_factory=list)
    error: str | None = None


def inspect_test(node):
    """Admit findings only after the entire function inspection succeeds."""
    findings = []
    units = list(assertions(node.body))
    if not units:
        return findings

    def add(line, detector, evidence):
        findings.append((line, detector, node.name, evidence))

    if all(guarded for _, _, guarded in units):
        add(node.lineno, "2-conditional-guard",
            "recognized assertions occur under one-sided guards; inspect possible no-assertion paths")
    for expr, line, _ in units:
        if same_operand(expr):
            add(line, "3-same-operand", "same-name equality operands; inspect independence and equality semantics")
    if claims_strong(node) and all(liveness(expr) for expr, _, _ in units):
        add(node.lineno, "7-oracle-name-on-smoke",
            "strong name/oracle marker with only recognized liveness checks; inspect the claimed behavior")
    return findings


def scan_file(path):
    result = ScanResult()
    try:
        with tokenize.open(path) as source:
            tree = ast.parse(source.read(), filename=str(path))
        result.parsed = True
        for node in named_tests(tree):
            result.findings.extend(inspect_test(node))
            result.tests += 1
    except Exception as err:
        # File-level failure boundary: keep completed evidence and continue the
        # batch, but never turn a failed inspection into a successful status.
        result.error = f"{path}: {type(err).__name__}: {err}"
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
        parsed += result.parsed
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
