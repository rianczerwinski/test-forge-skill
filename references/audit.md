# Audit mode — the redteam lens

Auditing a suite answers three questions: how much **redundancy** (the same truth established twice), how much **mismeasurement** (a test that does not measure what it claims), and how much **pointless effort** (a test that cannot fail or exercises nothing real). Mismeasurement is the dangerous one — a redundant test wastes time; a mismeasuring test manufactures false confidence and stays green through the regression it names.

## How to run an audit at scale

A large suite (100+ files) is beyond a single serial read. Fan out: cluster the test files by subsystem, hand each cluster to an agent with *this* rubric, and synthesize the findings with file:line evidence. Each cluster report returns: total LOC, test-fn count, a redundancy/waste estimate, a findings table, and a "biggest wins" list. `scripts/smell-scan.py` runs first to seed each agent with mechanical candidates.

Every finding carries: **file:line**, **kind-claimed vs kind-delivered**, **severity** (H/M/L), one-line **evidence**, and one **recommendation** (delete / merge / tighten / fix). Severity is driven by *danger*, not size: a can't-fail test on a critical path outranks a large redundant-but-honest suite.

## The seven category-collapse detectors

Each is a way a test claims a stronger kind than it delivers. Wrong→right pairs are in [../antipatterns.md](../antipatterns.md); this is the detection guide.

### 1. Circular golden
The golden was produced by the code under test. **Detect:** read the golden-generation script — does it import the module under test? Does the golden's docstring claim a "reference"/"oracle" origin the generator does not actually use? **Verdict:** it is a Regression test mislabeled Oracle. Relabel and stop counting it as correctness.

### 2. Conditional-guard can't-fail
Every assertion sits inside `if <precondition>:` — when the precondition is not met, the test runs zero assertions and passes. This gives false green on exactly the behavior it names (convergence, bootstrap, tracking). **Detect:** grep for asserts enclosed by an `if`; look for `if converged:`, `if segments:`, `if result is not None:` wrapping the only assertions. **Fix:** assert the precondition is reached first, then assert the magnitude.

### 3. In-test tautology
`expected` is recomputed by the same code under test, or the test reimplements the production logic inside itself and asserts on its own copy, or `assert x == x`. **Detect:** the same formula appears on both sides of the assertion; `assertTrue` wrapping an equality; a helper in the test file that mirrors the module. **Fix:** call the real code; source `expected` from a human or a reference.

### 4. Weakened-until-unfalsifiable
The assertion was loosened until it cannot fail: a tolerance far wider than the quantity's scale (`abs(x) < 1000` on a quantity near 1), an `in (A, B)` membership covering N-of-M outcomes, a range check that is always true (`0 <= azimuth < 360`). **Detect:** compare tolerance to the expected magnitude; flag membership asserts and full-range bounds. **Fix:** tighten to the noise floor, or assert the specific expected value.

### 5. Mock-shadow
The assertion checks a mock's own configured return value, so nothing real executed. **Detect:** the asserted value traces back to a `MagicMock(return_value=…)` set up in the same test. **Distinguish from legitimate contract tests:** asserting *which* handler was called with *which* payload (routing — including a bare `assert_called_once`) is a valid contract check; asserting that the mock returned what you told it to return is the smell. Three-way split: assert-the-mock's-return = shadow; assert-it-was-called = contract; assert-a-real-transform-of-the-mock's-output = legitimate. **Fix:** exercise the real path, or assert on the logic the production code applies to the mock's output.

### 6. Static-grep-as-behavior
A `re.search` / substring scan over source text, dressed as a behavioral test — passes or fails on formatting, not behavior. **Detect:** the test reads a `.py`/source file and regexes it. **Fix:** move to a CI lint, or write a real behavioral assertion.

### 7. Oracle-name-on-smoke
The name promises correctness (`test_localization_accuracy`, `test_separates_speakers`) while the body asserts only `not None` / `len > 0`. A common collapse, and easy to miss because the name reads as coverage. **Detect:** compare the strongest word in the test name to the strongest assertion in the body. **Fix:** rename to `_smoke`, or add the assertion the name promises.

## Redundancy patterns (the same truth, twice)

- **Episode-file vs permanent-suite overlap** — a migration/redteam-episode file re-tests what a subsystem suite already covers (or vice-versa: sometimes the episode file is the *only* real test and the "permanent" file is a smoke shell). Resolve by checking the source: if two files test the same symbol, keep the one with the stronger kind and delete the other.
- **Three-way smoke duplication** — the same shape/dtype/determinism template repeated across per-item files. Parametrize into one; keep the single oracle check that actually validates.
- **Verbatim fixture copies** — the same stub/fake/factory pasted across files. Hoist to a shared conftest.
- **Integration re-running unit convergence** — an integration test re-runs an expensive loop already proven at the unit level. Trim to a thin wiring assertion.

Not everything that looks redundant is: files that test *distinct code paths* (buffered vs streaming vs device-capture) or *distinct methods* (example-based vs property-based over the same function) are complements. Verify by code path before merging.

## Pointless effort (no failure, no real execution)

Dead helpers (zero call sites), meta-tests that exist only to test their own fixtures, standalone profiling scripts parked in the test dir and wired to no gate, expensive real-model or long-simulation runs whose only assertion is a shape check, trivial getter/dataclass/enum round-trips. Confirm dead code with a grep for call sites before deleting; downgrade expensive-but-vacuous runs to a cheap smoke or give them the assertion that justifies their cost.

## Output shape

A triaged, resumable catalog: a one-line suite summary (LOC, test-fn count, overall redundancy/waste estimate), a findings table sorted by severity, and a "biggest wins" list naming the specific deletions/merges/fixes that remove the most pointless effort and the most false confidence. Lead the wins with mismeasurement fixes (false confidence) over redundancy trims (wasted time).
