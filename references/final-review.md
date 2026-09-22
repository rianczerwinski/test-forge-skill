# Revision reasoning and validation

Implementation record: `20260908T100858Z`. The user approved the complete revision plan. The pre-change skill and original consultation remain recoverable at repository commit `481e850d4b12a5735a0380d1a095f2c233463f42`. This is a maintenance record, not a second operative procedure.

## Contents

- [Disposition of the consultation](#disposition-of-the-consultation)
- [Helper evidence](#helper-evidence)
- [Adversarial restoration checks](#adversarial-restoration-checks)
- [Behavioral and packaging checks](#behavioral-and-packaging-checks)
- [Bounded review repairs](#bounded-review-repairs--20260908t105028z)
- [Assurance calibration revision](#assurance-calibration-revision--20260922t174310)
- [Continuing limits](#continuing-limits)

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

The initial revision's dependency-free regression suite had 28 passing tests, with no skips on the implementation host. It covered genuine candidates, accepted legitimate shapes, async/class/nested functions, cardinality, repeated calls, numerical/membership judgment limits, malformed/mixed inputs, missing targets, decoding/reading/traversal failures, duplicate paths, extension filtering, no named tests, and special files that could otherwise block a scan. The bounded repair validation below supersedes these counts and hashes for the current helper.

Reproduction command from the skill directory:

```bash
python3 -B scripts/test_smell_scan.py
```

Initial validated helper SHA-256: `077c0f14a2dbd22bd6d509325773f3fc94b4298cb02d7e3bb528ff3ab25c440f`. Initial regression-source SHA-256: `6213af134cb92590383021630f44e0f9f2e1c0c4de8538d5749af7ea9a936fec`.

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

## Bounded review repairs — 20260908T105028Z

The reviewed initial revision remains recoverable at `cdbd5eb5a5c38c37acc4d971e31a6d203a0035ac`. Four localized findings prompted targeted repairs; the entrypoint, operating modes, and contextual judgment boundaries remain unchanged.

| Finding and consequence | Repair and rejected alternative | Validation |
|---|---|---|
| Recursive traversal of a valid 800-term module fixture aborted inspection and suppressed completed batch findings | Walk statement containers iteratively; admit one completed test at a time; report file-level exceptions with type/context and status 2 while retaining completed results. Reject increasing Python's recursion limit or merely discarding the file's prior evidence. | The deep-fixture CLI regression now inspects both files; injected mid-file failure preserves the completed test and later file, counts both parsed files but only completed tests, and reports the interrupted file. |
| Forced UTF-8 decoding rejected valid BOM/declared-encoding files; an unknown encoding declaration could conversely be ignored | Use Python's `tokenize.open`, not a bespoke detector or lossy decoding. | Valid BOM and Latin-1 fixtures compile and yield their candidates; unknown codecs, conflicting BOM/cookie, and undecodable bytes remain inspection errors. Python's compiler supplies an independent validity check for the encoding fixtures. |
| Failure categories were automatically discounted even when they were the tested behavior | Judge relevance to the named claim in the protocol and outcome table; distinguish missing-module importability rejection from unrelated plugin failure. | Fresh-context evaluation credited the former, withheld numerical sensitivity for the latter, and retained scope limits. |
| An ambiguous “keep or record” instruction could license deleting uncertain unique evidence | Retain until demonstrated replacement, or obtain explicit owner acceptance of the exact evidence gap; recording a follow-up alone grants no deletion authority. | Fresh-context evaluation retained uncertain restart evidence under ordinary refactor authority; explicit gap acceptance permitted removal without claiming redundancy or readiness. |

The unchanged 28-test baseline passed before editing the helper. Four selected new tests then reproduced the traversal, decoding, unknown-codec, and escaping-inspection-error behavior against the old helper (four assertion failures across subcases and one error). The final dependency-free suite has **35 passing tests** under both installed Python 3.9.6 and 3.14.4, with no skips. Additional statement-container cases protect definitions and assertions inside branches, exception handlers, cleanup blocks, loops, and context managers without admitting nested helper tests. Match-case syntax is assessed according to the running interpreter: inspected where supported, explicitly rejected as unsupported syntax on 3.9.

Five deliberate defects were applied individually in a separate copy after a passing selected baseline: unrestricted recursive traversal, rethrowing inspection errors, forced UTF-8 decoding, successful status after parse failure, and misclassifying both asserting branches as guarded. The relevant regressions rejected each for the intended observable defect. Every mutation was reversed with byte equality checked against the staged helper and its selected baseline rerun; the fully restored 34-test suite passed in 1.624 seconds. These are targeted regression protections, not a calibrated mutation score or runtime benchmark.

The first installed-path check selected Python 3.9.6 rather than staging's 3.14.4 and exposed two test-fixture failures: unconditional match syntax was not supported by the older interpreter. Separating that grammar-dependent case produced the 35-test suite; both interpreters then passed. The helper itself needed no runtime restriction. The packaging validator also lacked its own YAML dependency under 3.9, so it was run successfully with the existing 3.14 environment; no package or runtime configuration was installed or changed.

Current helper SHA-256: `f2809420527b61a0ec1360c1afa825d8ad37c9993fa693862bfe4c81b351ba64`. Current regression-source SHA-256: `77c0c04a4f67e0b98cdf792ece9dd8f59d5331e077f41dc06f5024e0572575ba`. Use the reproduction command above. One fresh-context evaluator assessed the four supplied guidance scenarios without intended answers or this record; no material ambiguity changed its dispositions. This checks interpretation of hypothetical observations, not execution of packaging or recovery tests.

Frontmatter, local links, paired examples, Python syntax, provider resolution, and the unchanged 124-line entrypoint passed packaging checks. `skills-ref` remained unavailable; the installed Skill Creator validator and direct checks supplied bounded packaging evidence. Source-decoding/traversal prior art is maintained in [lineage.md](lineage.md). The repairs add no dependency, production-suite change, or mandatory user workflow.

## Assurance calibration revision — 20260922T174310

The user requested a Test Forge revision incorporating the discussion of proportionate assurance and both Pagani dimensions. The source tree was clean within this skill at shared-shelf revision `818d8335a00e41e48274b880d036a34799368f1d`; unrelated repository changes were outside the concern. The existing domain and public-skill prior art was extended with primary assurance, stopping, decision-error, and evidence-dependence sources in [lineage.md](lineage.md).

| Requirement | Operative home and preservation decision |
|---|---|
| Reground the scale without another standalone skill | CALIBRATE in SKILL.md; [calibration.md](calibration.md); retained FORGE, AUDIT, and REFORGE |
| Address both insufficient protection and excessive burden | Entrypoint objective and calibration: consequences, existing controls, total burden, false rejection, and prevention value |
| Examine the criterion as well as assertion sensitivity | Decision/claim record, oracle reference, stable comparison criteria, protected qualities, and separation of observations/inferences/commitments |
| Ground deliberate false cases in real engineering failures | Potency guidance and bounded examples; no hypothetical malicious actor or universal mutation quota |
| Preserve independent authority and actual-use evidence | Default-entry-path guidance; source/mechanism/observation independence; explicit limits on repeated model agreement |
| Bound recursion and know when to stop | Named material doubt, different useful evidence, governing closure requirements, and distinct supported/failed/inconclusive outcomes |
| Preserve useful capabilities while simplifying | Existing bounded dominance rule plus prevention and diagnostic value; source/candidate preservation until replacement evidence exists |
| Preserve previous testing competence | Existing taxonomy, seam selection, double conformance, actual runner admission, oracle authority, RIPR potency, permitted alternatives, flaky evidence, budgets, and closure distinctions remain operative |

All pre-existing files were retained. Source-to-destination review of replaced passages found their substantive instructions preserved in the revised entrypoint; supporting changes were additive. Both Python files remained byte-identical to the baseline. The historical audit, refactor, and potency examples retain their original measurements and limits. Six constructed calibration examples and six paired antipatterns supply maintenance cases without claiming executable validation of judgment.

### Behavioral forward check

One fresh-context read-only evaluator received the staged entrypoint and access to operative references, plus eight hypothetical requests. It did not receive this conversation, intended answers, examples, antipatterns, or this record. Skill Creator's conditional forward-test procedure supplied the review method.

| Supplied case | Observed judgment |
|---|---|
| Unchanged two-second parser test run | FORGE run-only; inspect selector/gates, execute within authority, report actual outcomes; no added assurance ceremony |
| Moved link with repository-mandated falsification | Resolve target/anchor and reject an isolated broken link; preserve the rule without building a framework |
| Passing DSP components with untested default command | Withhold operational sign-off; observe the assembled default path and bound liveness versus quality claims |
| Mocked export acknowledgement before deleting the only original | Treat preservation as consequential; prefer eliminating premature deletion and use real-storage evidence with disposable content |
| Faster suite, relaxed tolerance, protected regression, quiet recovery test | Keep criteria comparable, surface the protected failure, and retain unique recovery protection until a replacement earns its role |
| Repeated agent approval of a migration summary | Change the source evidence examined; compare source qualifications with destinations before deletion; no confidence multiplier |
| Five successful cases at budget limit with required devices missing | Stop the run within authority; keep the reliability requirement inconclusive |
| Shared fixture fault affecting five modules | Investigate the implicated family and regression protection; neither stop after one passing test nor automatically audit everything |

The evaluator found no consequential ambiguity in the operative instructions it reviewed. This is one qualitative interpretation exercise over eight scenarios, not eight independent trials, a comparison against the previous skill, or execution of those scenarios. Final editorial changes scoped the trigger to engineering and clarified required-content preservation in the example; neither changes the evaluated method.

### Structural and regression checks

The installed Skill Creator frontmatter validator passed on the staged skill. Direct structural checks resolved local destinations and anchors, confirmed all 15 supporting resources are indexed from the 142-line entrypoint, and checked all 27 paired antipatterns. In an isolated copied tree, a nonexistent calibration link was rejected by the link check and an invalid skill name by the actual frontmatter-validator CLI. The copied tree was discarded after these observations; no production files were mutated.

The unchanged helper's actual regression entry point, `python3 -B scripts/test_smell_scan.py`, passed all 35 tests without skips on the implementation host. This confirms retained helper behavior; it supplies no validation of the new prose's real-world effectiveness. `skills-ref` was unavailable, so no result from that tool is claimed. No new executable, dependency, schema, controller, or workflow engine was introduced.

Trigger review covered running existing tests, writing a boundary test, auditing a misleading suite, refactoring expensive setup, calibrating excessive assurance, designing a migration checker, and deciding when a reliability run can stop. Countertriggers were general product positioning, emotional reassurance, and whole-system readiness without a bounded apparatus question; those remain outside this skill or route to the appropriate upstream method. This is metadata review, not measured discovery recall.

## Continuing limits

The scanner remains a Python syntactic candidate generator, with deliberately limited control-flow and assertion recognition; it does not perform runner collection, semantic redundancy analysis, or oracle validation. Its errors now remain explicit, but precision/recall on an independent real-suite population is uncalibrated.

The procedure's broader real-world effectiveness likewise requires independent live use. The retained scenario evidence establishes the behaviors described above, not universal compliance by future agents. Provider adapters resolve the canonical shelf; no separate provider copy or configuration change is required.
