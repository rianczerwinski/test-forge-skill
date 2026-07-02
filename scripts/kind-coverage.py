#!/usr/bin/env python3
"""Report source modules that lack a required test *kind*.

Enforces the required-kinds rule (references/taxonomy.md §3): a numeric module
must carry Oracle + Property tests; a stateful module Property + Contract; IO/CLI
Contract + Smoke. Coverage percentage cannot see this — a module can be 100%
line-covered by tests that only establish liveness. This script reads the *kind
markers* on tests and cross-references which source module each test targets.

It is deliberately convention-driven, not magic: you tell it (a) how tests are
marked with their kind, and (b) how a test maps to the source module it tests.
Both are project decisions — the defaults below are a starting template, and
every default is justified inline. Adjust to your suite, don't fight it.

Usage:
    python3 kind-coverage.py --src src/pkg --tests tests \
        --require "numeric:oracle,property" --require "io:contract,smoke"

Marking convention (default): a test declares its kind with a pytest marker,
`@pytest.mark.oracle` / `.property` / `.regression` / `.contract` / `.smoke`.
Mapping convention (default): a test file `tests/**/test_<mod>.py` targets the
source module `<mod>` — matched by basename. Override --map-strategy if your
layout mirrors the source tree path instead (recommended for large suites).

This is an ADVISORY tool by default (exit 0 with a report). Pass --gate to exit
nonzero when any module is missing a required kind, for CI.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

KINDS = {"oracle", "property", "regression", "contract", "smoke"}

# A kind marker on a test. Matches @pytest.mark.<kind> and @mark.<kind>.
MARK_RE = re.compile(r"@(?:pytest\.)?mark\.(" + "|".join(KINDS) + r")\b")
# A test function definition — used to attribute nearby markers to a real test.
DEF_RE = re.compile(r"^\s*def (test_\w+)")
# Map a test filename to the source-module stem it targets: test_<stem>.py
FILE_MOD_RE = re.compile(r"test_(.+)\.py$")

# The module-character buckets. A source module is bucketed by matching its path
# against these substrings, first match wins. This is the crudest possible
# classifier and is meant to be replaced by an explicit map for a real project;
# it exists so the tool runs with zero config on a conventionally-laid-out repo.
DEFAULT_BUCKETS = [
    ("numeric", ("inference", "frontend", "calibration", "enhancement", "solver", "ops", "dsp")),
    ("stateful", ("streaming", "tracker", "ekf", "scheduler", "diariz")),
    ("io", ("io", "storage", "protocol", "audio", "wav", "codec")),
    ("cli", ("cli", "command")),
]


def kinds_per_module(tests_dir: Path, map_strategy: str) -> dict[str, set[str]]:
    """module-stem -> set of kinds that at least one of its tests declares."""
    result: dict[str, set[str]] = defaultdict(set)
    for path in sorted(tests_dir.rglob("test_*.py")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as err:
            print(f"warn: skip {path}: {err}", file=sys.stderr)
            continue
        if map_strategy == "path":
            # mirror layout: tests/unit/frontend/test_music.py -> frontend/music
            rel = path.relative_to(tests_dir)
            m = FILE_MOD_RE.search(path.name)
            stem = str(rel.parent / m.group(1)) if m else str(rel.parent)
        else:  # "basename" (default)
            m = FILE_MOD_RE.search(path.name)
            stem = m.group(1) if m else path.stem
        for kind in MARK_RE.findall(text):
            result[stem].add(kind)
        # A file with tests but no kind markers is itself a finding: unmarked.
        if not MARK_RE.search(text) and DEF_RE.search(text):
            result[stem].add("UNMARKED")
    return result


def bucket_of(module_path: str, buckets) -> str:
    low = module_path.lower()
    for name, needles in buckets:
        if any(n in low for n in needles):
            return name
    return "other"


def main() -> int:
    ap = argparse.ArgumentParser(description="Report modules missing a required test kind.")
    ap.add_argument("--src", type=Path, required=True, help="source root")
    ap.add_argument("--tests", type=Path, required=True, help="tests root")
    ap.add_argument(
        "--require",
        action="append",
        default=[],
        metavar="BUCKET:kind,kind",
        help="required kinds per bucket, e.g. numeric:oracle,property (repeatable)",
    )
    ap.add_argument("--map-strategy", choices=("basename", "path"), default="basename")
    ap.add_argument("--gate", action="store_true", help="exit nonzero on any gap")
    args = ap.parse_args()

    for p in (args.src, args.tests):
        if not p.exists():
            print(f"error: {p} does not exist", file=sys.stderr)
            return 2

    # Parse --require into {bucket: {kinds}}; fall back to sane defaults.
    required: dict[str, set[str]] = {}
    for spec in args.require:
        try:
            bucket, kinds = spec.split(":", 1)
            required[bucket] = {k.strip() for k in kinds.split(",") if k.strip()}
        except ValueError:
            print(f"error: bad --require {spec!r} (want BUCKET:kind,kind)", file=sys.stderr)
            return 2
    if not required:
        required = {
            "numeric": {"oracle", "property"},
            "stateful": {"property", "contract"},
            "io": {"contract", "smoke"},
            "cli": {"contract", "smoke"},
        }

    have = kinds_per_module(args.tests, args.map_strategy)

    gaps: list[str] = []
    unmarked: list[str] = []
    unclassified: list[str] = []  # matched no bucket → NO floor applies → the gate is blind to it
    src_modules = [p for p in args.src.rglob("*.py") if p.name != "__init__.py"]
    for mod in sorted(src_modules):
        stem = str(mod.relative_to(args.src).with_suffix("")) if args.map_strategy == "path" else mod.stem
        bucket = bucket_of(str(mod), DEFAULT_BUCKETS)
        present = have.get(stem, set())
        if "UNMARKED" in present:
            unmarked.append(f"{stem}  (has tests, none declare a kind)")
        if bucket not in required:
            # No floor: the gate cannot flag this module. Surface it — a numeric core
            # module in a dir whose name lacks a bucket keyword lands here and would
            # otherwise escape the gate SILENTLY (a false all-clear).
            unclassified.append(f"{stem}  (bucket '{bucket}' has no required floor — assign one if this is core)")
            continue
        missing = required[bucket] - present
        if missing:
            gaps.append(f"{stem}  [{bucket}]  missing: {', '.join(sorted(missing))}  (has: {', '.join(sorted(present - {'UNMARKED'})) or 'none'})")

    print(f"# kind-coverage over {len(src_modules)} source modules\n")
    if unmarked:
        print(f"## {len(unmarked)} file(s) with unmarked tests (classify these first):")
        for u in unmarked:
            print(f"  {u}")
        print()
    if gaps:
        print(f"## {len(gaps)} module(s) below their required-kinds floor:")
        for g in gaps:
            print(f"  {g}")
    else:
        print("## all bucketed modules meet their required-kinds floor")
    if unclassified:
        print(f"\n## {len(unclassified)} module(s) the gate cannot see (no bucket matched):")
        for u in unclassified:
            print(f"  {u}")
        print("  → these are NOT 'all clear' — they simply have no floor. Bucket the core ones.")

    if args.gate and (gaps or unmarked):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
