# Revision reasoning and validation

Implementation record: `20260908T100858Z`. The user approved the complete revision plan. The pre-change skill and original consultation remain recoverable at repository commit `481e850d4b12a5735a0380d1a095f2c233463f42`. This is a maintenance record, not a second operative procedure.

## Disposition of the consultation

| Concern | Implemented home | Reasoning and rejected alternative |
|---|---|---|
| Decision, claim source, and bounded experiment | SKILL.md decision/claim record and decision-before-cost gate; audit reference; potency example | Prevents an oversized experiment even when individual assertions are strong. Preserves contextual sample sizing instead of prescribing two cases or a matrix. |
| Individual potency and valid alternatives | Shared [potency.md](potency.md); grouping example; revised anti-patterns | Uses activation, propagation, observation, and permitted equivalence. Avoids treating coverage, label count, or a generic mutant score as adequacy. |
| Safe and interpretable falsification | Potency protocol and outcome table | Isolated changes, nonempty baseline, expected-reason rejection, exact restoration. Allows relevant pre-fix evidence instead of repeated mutation ceremony. |
| Oracle absolutes and double fidelity | [oracles.md](oracles.md) and taxonomy | Authority, correlated mechanisms, claim relevance, and error budgets govern strength. Removes blanket snapshot/mocking/tolerance rules. |
| Bounded reduction and closure | [audit.md](audit.md), reforge, and SKILL.md closure states | Preserves input/history/environment and negative-control roles. Capturing a gap completes neither its repair nor readiness. |
| Flaky evidence and execution admission | Audit reference and SKILL.md execution guidance | Initial failures and retries remain distinct; quarantine has ownership/exit conditions. Missing environments and failed inspection cannot appear as passed evidence. |
| Scanner false confidence | [smell-scan.py](../scripts/smell-scan.py) and [test_smell_scan.py](../scripts/test_smell_scan.py) | Retains three syntax candidate families; removes unsupported range/tolerance/membership/mock dataflow judgments and dead code. Explicit error status replaces a misleading successful summary. |
| Adjacent skill boundaries and prior art | SKILL.md routing and [lineage.md](lineage.md) | Retains FORGE/AUDIT/REFORGE without duplicating systemic assurance, repository organization, or provider-management procedures. |
| Reasoning preservation and stale guidance | This record, maintained lineage, paired examples | Incorporates the consultation's guidance into its canonical homes, retaining rationale and validation rather than a parallel pending instruction set. |

The governing tradeoffs remain observable: a whole-system readiness claim calls for the upstream census; repeated escaped faults can justify deeper mutation work; an independently evaluated scanner whose review cost exceeds useful discoveries should be reduced further or removed. No universal sample size, error threshold, mutation quota, or audit-document requirement was introduced.

## Helper evidence

The original helper's SHA-256 was `a3cc2c269056d58fc58038e897491d389f47e34e59c5ad70d3b64d4a201bfe1a`. Four targeted regression tests were run against it before the fix. All four failed for the reproduced behavior:

- Both if/else branches asserting: falsely reported a possible assertion-free path.
- Tight numeric interval: falsely called an unfalsifiable full-range bound.
- Mock callback routing: falsely treated as configured-return-value evidence.
- Invalid Python: warning and successful no-candidates exit instead of incomplete inspection.

The dependency-free regression suite now has 28 passing tests, with no skips on the implementation host. It covers genuine candidates, accepted legitimate shapes, async/class/nested functions, cardinality, repeated calls, numerical/membership judgment limits, malformed/mixed inputs, missing targets, decoding/reading/traversal failures, duplicate paths, extension filtering, no named tests, and special files that could otherwise block a scan.

Reproduction command from the skill directory:

```bash
python3 -B scripts/test_smell_scan.py
```

Validated helper SHA-256: `077c0f14a2dbd22bd6d509325773f3fc94b4298cb02d7e3bb528ff3ab25c440f`. Regression-source SHA-256: `6213af134cb92590383021630f44e0f9f2e1c0c4de8538d5749af7ea9a936fec`.

## Adversarial restoration checks

Both probes ran in a separate temporary copy with the same selected tests. The unchanged pair first passed.

| Deliberate change | Selected regression | Observed rejection |
|---|---|---|
| Return 0 rather than 2 from the incomplete-inspection branch | `ScannerTests.test_syntax_failure_is_incomplete_inspection` | Assertion rejected actual exit 0 versus required 2; parsing still reported its error, so this was the intended status failure |
| Treat every if/else branch as guarded | `ScannerTests.test_both_branches_assert` | Assertion rejected an unwanted conditional candidate for a valid both-branches fixture |

Each mutation was restored by exact patch reversal, followed by byte comparison against the staged helper. The fully restored 28-test suite passed. These are two demonstrated regression protections, not an overall mutation score.

## Behavioral and packaging checks

One fresh-context, read-only evaluator applied the staged skill to five supplied scenarios without receiving intended answers or the consultation record:

| Scenario | Observed behavior |
|---|---|
| Existing fast parser tests, run-only request | Selected ordinary execution; introduced no claim-map or mutation exercise; refused to invent an unobserved result |
| Speaker assignment with arbitrary labels | Compared grouping, accepted relabeling, proposed wrong-grouping controls, separated oracle discrimination from system detection |
| Capability check with a proposed 6 × 24 × 12-minute matrix | Identified survey-sized work; computed 108 worker-hours / about 36 idealized elapsed hours from supplied throughput; requested relevant case/criterion/bound rather than imposing a count |
| Slow HTTP validation apparatus | Moved irrelevant model cost outward, retained socket and model-quality roles, identified hidden slow-test exclusion, respected unchanged-production scope |
| Whole-system release readiness with skipped recovery evidence | Withheld readiness and routed upstream risk census to Audit Planes; preserved the owner data-survival requirement |

These are five qualitative scenario checks in one evaluator context, not five independent reliability trials. No production suites, downloads, or external services were exercised.

The executable partition example accepted correct relabelings and rejected collapsed, alternating, and shortened outputs. The frontmatter validator passed; local links resolve; new resources are indexed directly from SKILL.md; paired examples and Python syntax were checked. SKILL.md is 124 lines. `skills-ref` was unavailable, so packaging validation used the installed Skill Creator validator plus direct checks rather than claiming that tool ran.

## Continuing limits

The scanner remains a Python syntactic candidate generator, with deliberately limited control-flow and assertion recognition; it does not perform runner collection, semantic redundancy analysis, or oracle validation. Its errors now remain explicit, but precision/recall on an independent real-suite population is uncalibrated.

The procedure's broader real-world effectiveness likewise requires independent live use. The retained scenario evidence establishes the behaviors described above, not universal compliance by future agents. Provider adapters resolve the canonical shelf; no separate provider copy or configuration change is required.
