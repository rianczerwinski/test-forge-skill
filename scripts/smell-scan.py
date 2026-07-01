#!/usr/bin/env python3
"""Seed a test-suite audit with mechanical category-collapse candidates.

Heuristic, not a judge: every hit is a *candidate* a human (or an audit agent)
must confirm — the patterns intentionally over-flag, because a false positive
costs one glance while a false negative hides a mismeasuring test. Output is
grouped by detector with file:line so it can be pasted into an audit rubric.

Detectors map to references/audit.md §"The seven category-collapse detectors".
Only the mechanically-detectable ones are here; circular-golden and
in-test-tautology need semantic reads and are left to the human pass.

Usage:
    python3 smell-scan.py <tests_dir> [--ext .py]

Language note: the regexes target Python/pytest idioms. For jest/vitest/go,
adjust ASSERT_RE and the guard/range patterns — the detector *concepts* are
language-agnostic; only the surface syntax here is Python.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# An assertion line — pytest bare assert or unittest self.assert*.
ASSERT_RE = re.compile(r"^\s*(assert\b|self\.assert)")

# Detector 4a: full-range bound that cannot fail. A membership/range check whose
# bounds are the definition of the quantity (0<=az<360, 0<=p<=1 on a probability).
# Flags comparisons chained around a value with numeric literals on both sides.
RANGE_ALWAYS_TRUE = re.compile(
    r"assert\s+-?\d+(?:\.\d+)?\s*<=?\s*\w+\s*<=?\s*-?\d+(?:\.\d+)?"
)

# Detector 4b: membership assert (`in (A, B)`) — N-of-M outcomes, often weakened.
MEMBERSHIP = re.compile(r"assert\s+\w+(?:\.\w+)*\s+in\s+[\(\[{]")

# Detector 4c: suspiciously wide tolerance. atol/rtol/abs(...) < BIG.
# 10.0 is the threshold: DSP/embedding quantities are typically O(1)–O(10), so a
# tolerance >= 10 on a comparison is nearly always unfalsifiable. Tune per domain.
WIDE_TOL = re.compile(r"(atol|rtol)\s*=\s*(\d+(?:\.\d+)?)")
WIDE_TOL_THRESHOLD = 1.0

# Detector 5: mock-shadow — assert on *_called* only, or a MagicMock return_value.
MOCK_CALLED = re.compile(r"assert.*\.(assert_called|called|call_count)\b|\.assert_called")
MOCK_RETURN = re.compile(r"(MagicMock|Mock)\s*\(\s*return_value")

# Detector 6: static-grep-as-behavior — reading source text and regexing it.
STATIC_GREP = re.compile(r"\.read_text\(\)|re\.(search|match|findall)\(")

# Detector 7: oracle-name-on-smoke. A test whose name promises correctness but
# whose body's only assertion is a liveness check. Handled with a two-pass scan.
STRONG_NAME = re.compile(
    r"def (test_\w*(accura|correct|matches|recover|localiz|separat|equival|converg)\w*)"
)
SMOKE_ASSERT = re.compile(
    r"assert\s+\w[\w.]*\s+is\s+not\s+None\s*$|assert\s+len\([^)]+\)\s*(>=?\s*[01]|!=\s*0)\s*$"
)

# Detector 2: conditional-guard can't-fail — an `if` whose body's only statements
# are assertions. Detected structurally in scan_guards() by indentation.
IF_RE = re.compile(r"^(\s*)if\s+.+:\s*$")


def scan_line_patterns(path: Path, lines: list[str]) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        if RANGE_ALWAYS_TRUE.search(line):
            hits.append((i, "4-unfalsifiable-range", line.strip()))
        if MEMBERSHIP.search(line):
            hits.append((i, "4-membership-assert", line.strip()))
        for m in WIDE_TOL.finditer(line):
            if float(m.group(2)) >= WIDE_TOL_THRESHOLD:
                hits.append((i, "4-wide-tolerance", line.strip()))
        if MOCK_CALLED.search(line) or MOCK_RETURN.search(line):
            hits.append((i, "5-mock-shadow", line.strip()))
        if STATIC_GREP.search(line) and "read_text" in line:
            hits.append((i, "6-static-grep", line.strip()))
    return hits


def scan_guards(lines: list[str]) -> list[tuple[int, str, str]]:
    """Flag an `if` whose entire indented body is assertions (or pass) — the
    conditional-guard can't-fail shape. Approximate: looks one block ahead."""
    hits: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines):
        m = IF_RE.match(line)
        if not m:
            continue
        indent = len(m.group(1))
        body: list[str] = []
        for nxt in lines[i + 1 :]:
            if not nxt.strip():
                continue
            nxt_indent = len(nxt) - len(nxt.lstrip())
            if nxt_indent <= indent:
                break
            body.append(nxt.strip())
        if body and all(
            b.startswith(("assert", "self.assert", "pass")) for b in body
        ):
            hits.append((i + 1, "2-conditional-guard", line.strip()))
    return hits


def scan_name_vs_body(lines: list[str]) -> list[tuple[int, str, str]]:
    """Detector 7: a strongly-named test whose asserts are all liveness."""
    hits: list[tuple[int, str, str]] = []
    text = "".join(lines)
    for nm in STRONG_NAME.finditer(text):
        start = text[: nm.start()].count("\n") + 1
        # gather the function body's assertion lines until the next def/class
        body_lines = []
        for j in range(start, len(lines)):
            ln = lines[j]
            if j > start and re.match(r"^\s*(def |class )", ln):
                break
            if ASSERT_RE.match(ln):
                body_lines.append(ln.strip())
        if body_lines and all(SMOKE_ASSERT.search(b) for b in body_lines):
            hits.append((start, "7-oracle-name-on-smoke", nm.group(1)))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Mechanical test-smell candidate scanner.")
    ap.add_argument("tests_dir", type=Path)
    ap.add_argument("--ext", default=".py")
    args = ap.parse_args()

    if not args.tests_dir.exists():
        print(f"error: {args.tests_dir} does not exist", file=sys.stderr)
        return 1

    grouped: dict[str, list[str]] = {}
    files = sorted(args.tests_dir.rglob(f"*{args.ext}"))
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        except (OSError, UnicodeDecodeError) as err:
            print(f"warn: skip {path}: {err}", file=sys.stderr)
            continue
        flat = [ln.rstrip("\n") for ln in lines]
        hits = (
            scan_line_patterns(path, flat)
            + scan_guards(flat)
            + scan_name_vs_body(lines)
        )
        for lineno, detector, evidence in hits:
            grouped.setdefault(detector, []).append(
                f"{path}:{lineno}  {evidence[:100]}"
            )

    if not grouped:
        print("no mechanical smell candidates found (semantic detectors still need a human pass)")
        return 0

    total = sum(len(v) for v in grouped.values())
    print(f"# {total} candidate(s) across {len(files)} files — CONFIRM each; heuristics over-flag.\n")
    for detector in sorted(grouped):
        print(f"## {detector}  ({len(grouped[detector])})")
        for entry in grouped[detector]:
            print(f"  {entry}")
        print()
    print("Not detected mechanically (need a human/agent read): circular goldens, in-test tautologies, episode-file redundancy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
