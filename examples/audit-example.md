# Worked example — auditing a suite

A condensed, illustrative walkthrough of a real audit of a numpy-only DSP/ML library's test suite — findings are paraphrased to show the *method and output shape*, not reproduced with their original file:line citations (the real catalog carried those). Treat the specific claims here as representative, not as a checkable record.

## Input

`relata` — 130 test files, ~38k test LOC against ~35k source LOC (1.08:1). The prompt: *how much redundancy, how much mismeasurement, how much pointless effort.*

## Method

The suite was too large to read serially, so: cluster the 130 files by subsystem (neural/ops, spatial/calibration, EKF/fusion/streaming, ASR/transcript, infra/CLI), hand each cluster to an agent with the seven-detector rubric from [../references/audit.md](../references/audit.md), and synthesize with file:line evidence. `smell-scan.py` seeded the mechanical candidates first.

## Output — findings, by the three questions

**Redundancy (~15–18%, structurally concentrated).** Not scattered — it clustered in recognizable shapes:
- *Episode-file vs permanent-suite overlap*, with a twist: `SRPLocalizer = SRPLocalizerNP` (a source alias) meant three "permanent" files (`test_srp_phat`, `test_music`, `test_calibration`) were one-line `assert isinstance(result, list)` shells testing the *same class* that the migration-era `test_wave1c_doa.py` covered with real accuracy assertions. **The episode file was the keeper; the permanent files were the dead scaffolding** — the inverse of the usual guess. Verdict required reading the source, not the filename.
- *Three-way smoke duplication* — ECAPA shape/norm/determinism asserted in three files.
- *Verbatim fixture copies* — a fake model copied across three ASR files; six near-identical stub providers.

**Mismeasurement (smaller, dangerous).** Ranked by deception:
- *Circular goldens* — `test_golden_refs.py` asserted numpy output bit-exactly equals a golden generated *by that same numpy code*, with a docstring claiming "ONNX oracles." False. Regression mislabeled Oracle.
- *In-test tautologies* — `residual = (d_b-d_a)/c - tdoa_obs` where `tdoa_obs` *is* `(d_b-d_a)/c`; a `test_pyannote` that reimplemented the segmenter's aggregation inside the test and asserted on its own copy.
- *Conditional-guard can't-fail* — assertions wrapped in `if converged:` / `if phase >= EKF_TRACKING:`, going green on exactly the non-convergence they named.
- *A gate test proving its opposite* — `test_capture_device_cannot_rename` asserted the rename **succeeds**.
- *Weakened-until-unfalsifiable* — `assert regime in (STATIC, WALKING)` (2-of-4), `assert 0 <= az < 360`.
- *Silently-skipped correctness* — the only validation of a hand-rolled DSP kernel skipped in every CI run because its reference dep wasn't installed.

Myth busted by the audit: the mock-heavy ASR tests were checked specifically and found to assert *routing* (which speaker gets which text), a legitimate contract use — not mock-shadow. Don't flag on "uses a mock"; flag on "asserts the mock's own return value."

**Pointless effort (~12–15%).** Dead helpers (zero call sites, confirmed by grep), meta-tests existing only to test their own fixtures, a 630-LOC profiling script parked in `tests/` wired to no gate, a real-model test that pulled 75 MB to transcribe *silence* and assert only list-shape.

## The three biggest wins (led with false-confidence, not waste)

1. **Fix the false coverage map** — relabel the circular goldens, delete the tautologies, unwrap the conditional guards. ~250 LOC, highest stakes: this is where a real regression currently passes green.
2. **Collapse the episodes into the subsystems** — delete the smoke shells, dedupe fixtures to conftest, drop workstream IDs from docstrings. ~1,500–2,000 LOC, mechanical.
3. **Resolve the silent skips and dead weight** — add the missing reference dep so the equivalence check runs; delete confirmed-dead code.

## What made it an audit and not a vibe

Every finding had file:line, a kind-claimed-vs-delivered judgment, a severity driven by danger (a can't-fail test on a critical path outranked a large honest-but-redundant suite), and one recommendation. The strong parts were named too — the op-correctness suites with hand-computed expecteds, the EKF tolerance test *with a negative control* — so the user could calibrate, not just cut.
