# Test Forge final consultation

Review stamp: `20260908T093302Z`. Reviewed repository revision: `d9de27a761cdf19e3978d3a553a25210a59f76aa`; Test Forge was clean at inspection. This record preserves recommendations and evidence for the next revision. It does not amend the operative procedure or assert that the pending work is implemented.

## Outcome

Retain the current claim → failure → authority → seam → execution → evidence structure. The remaining work is a bounded correction of potency, experimental admission, evidence limits, and the helper's behavior. Another wholesale taxonomy or audit package is not warranted by this review. Completion of this consultation means its findings are captured; it does not establish readiness of the existing helper or validate the skill's real-world effectiveness.

## Advisory panel

This is a single-context synthetic panel, not consultation with actual professionals or independent validation. Its voices optimize for different outcomes: QA for missed-defect detection; maintenance for useful refactor freedom; SRE for truthful execution states; experimental design for decision-relevant evidence; formal methods for bounded claims; skill authorship for proportional effort.

The QA and formal-methods lenses converge on explicit potency evidence for different reasons: one needs faults detected, the other needs the conclusion limited to what was demonstrated. Maintenance and skill authorship converge on lightweight ordinary use: one avoids brittle tests, the other avoids procedural overhead. Their unresolved tension concerns when those checks deserve a written record.

| Axis | Proposed default | Closest challenger and dissenter | Observable flip condition |
|---|---|---|---|
| Potency effort | A brief claim-specific check; write the record for consequential new evidence or apparatus redesign | Formal-methods lens: written trace for every changed critical claim | The change governs irreversible loss, a release assurance claim, or a missed defect whose cause was an unexamined oracle |
| Failure discovery | Derive the relevant boundary and state paths inside the requested scope | QA lens: upstream Audit Planes census | Claimed closure covers a whole system, or findings show shared infrastructure invalidates the bounded scope |
| Mutation investment | Relevant pre-fix failure or a targeted isolated falsifier, plus triage | QA lens: automated mutation campaign | Repeated escaped faults survive the targeted checks and a bounded pilot shows useful additional detections |
| Static helper scope | Retain only defensible syntactic candidate detection; make partial inspection explicit | Minimalist skill-author lens: remove the helper | A labeled pilot finds that review and maintenance cost exceed useful candidate discovery |

The experimentalist's objection is independent of these axes: an impeccable test can still belong to the wrong experiment. An expensive run needs a decision and sampling argument before launch. Adding stronger assertions alone cannot prevent another oversized capability gate.

## Updated skill-store composition

The current canonical store and provider adapters were inspected, including the working-tree version of adjacent skills. No adjacent skill was modified by this consultation.

- **Audit Planes:** owns whole-codebase risk topology and independently grounded assurance. Its separation of schema/contract validity from evidential validity belongs in Test Forge's closure language. Same-run planted mutants do not calibrate recall against unseen defects.
- **Redteam:** owns bounded adversarial review under the actual operating conditions. Its conversational default argues against mandatory audit files for a small test change.
- **Repo Refiner:** owns physical repository structure and navigation; it supersedes older repository-refinement naming. Test Forge may identify ownership problems without duplicating its tree-management procedure.
- **Closeout:** owns unresolved-work capture and commit sequencing. Captured proof gaps survive a session; they remain gaps.
- **Skill-skill:** canonical shared authorship and provider discovery remain its responsibility. Test Forge has no reason to reproduce installation or adapter-management instructions.

Claude Code's Test Forge adapter resolves to the canonical shelf; Antigravity's shelf adapter resolves there too. Codex discovers the canonical shelf directly. No separate editable provider copy was found in the inspected locations.

## Pending revision findings

All items below remain open recommendations. The record preserves them without claiming user assent to the proposed defaults.

### Decision and scope before execution

Add the decision served by the run, claim source/status, scope bounds, and excluded claims. Distinguish owner/specification commitments from inferred risks and historical behavior. Before an expensive baseline or matrix, state pass/fail/inconclusive actions, the first informative batch, measured throughput and cost bound, and conditions for expansion. Reuse identical results only when code, configuration, inputs, and evidence identity remain compatible. A small capability demonstration does not establish reliability over a population; neither two cases nor a full matrix is a universal default.

Derive failures from actual state and boundary paths. Omission, corruption, duplication, ordering, timing, partial persistence, stale identity, unauthorized access, and recovery are prompts where relevant, not a compulsory Cartesian checklist. Include meaningful interactions and selection impact through fixtures, shared configuration, and workflows. One potent test does not establish a complete failure population.

### A test's potency includes valid behavior

Make the check explicit: does the setup reach and activate the fault; does the wrong state survive to an observed result; does the oracle reject it; and does the test accept permitted alternatives? For example, merely finding two distinct speaker labels does not establish correct speaker assignment. A valid relabeling must remain acceptable while incorrect grouping is rejected.

Evaluate double fidelity when a conclusion depends on the double representing a real dependency. Do not require a separate conformance campaign for every trivial callback or stub. A wrapper returning its collaborator's value can be a legitimate contract claim even when that value comes from a mock.

### Mutation must fail for the claimed reason

Use an isolated copy where possible; preserve existing user changes. Establish a nonempty baseline, verify the intended perturbation was applied, identify the expected behavioral rejection, and distinguish that rejection from syntax, import, collection, setup, or unrelated failures. Restore the exact original bytes. A timeout counts according to the claim being tested, not automatically as a useful kill. Equivalent mutants and working fallbacks require analysis; survival is not automatically an inert oracle. Relevant historical pre-fix failure can supply evidence without a new mutation ritual on every routine run.

### Correct the oracle guidance's absolutes

`references/oracles.md` currently says differential and metamorphic tests are stronger than any snapshot, that disabling a mechanism while the test passes establishes an inert oracle, and that a tolerance ten times a quantity cannot fail and should be tightened to the noise floor. These statements are too strong. Authority and relevance decide strength; equivalent behavior or fallback can explain survival; tolerances need units, an engineering error budget, expected variability, and consequential error cases.

Likewise, matching a reference is a scoped conformance claim, not the only correctness obligation a model port can have. Sharing unrelated infrastructure does not necessarily destroy generator independence; shared mechanisms capable of reproducing the same error are the concern. Capture-once fixtures with a separately runnable live reference check are an option, not an unconditional default.

### Bound closure and reduction claims

Describe properties as evidence over exercised inputs unless exhaustive or formal reasoning establishes more. An independent reference can itself be wrong. Separate audit completion, test-task completion, and system readiness; recording a gap does not discharge it. Document only applicable execution planes. Replace the seam ladder's implied universal order with a palette of independently relevant boundaries.

A deletion argument must identify its supported fault families, inputs, histories, environments, cadence, and diagnostic roles. Representative mutants strengthen that argument but do not establish universal equivalence. Retirement of a requirement needs owner authority separately from elimination of redundant evidence.

### Give flaky evidence an explicit disposition

Retain the first failing attempt and report retries separately. Distinguish product races from harness faults, shared state, order dependence, resource contention, and timing. Retain the relevant input, seed, history, and environment; a seed alone may not replay a failure. Quarantine needs a named follow-up and exit condition and remains a proof gap.

### Repair the scanner before relying on its summaries

Reviewed helper SHA-256: `a3cc2c269056d58fc58038e897491d389f47e34e59c5ad70d3b64d4a201bfe1a`.

Direct in-memory probes loaded the actual helper with Python bytecode writing disabled, substituted `Path.read_text` with each source below, and called `scan_file`. For the syntax case, `main` received one gathered file containing invalid syntax. These probes characterize specific defects; they are not an estimate of overall scanner precision or recall.

| Fixture | Observed result | Problem |
|---|---|---|
| `if x: assert x == 1` / `else: assert x == 0` inside one test | `2-conditional-guard` | Both branches assert; the claimed zero-assert path is absent |
| `assert 0.49 < p < 0.51` as the sole assertion | `4-unfalsifiable-range` | A tight acceptance interval is classified as an unfalsifiable full-range bound |
| `callback = MagicMock(return_value=3); dispatch(callback); callback.assert_called_once()` | `5-mock-shadow-return` | Routing verification is confused with checking a configured return value |
| File containing `def test_broken(:` | Warning, then no-candidates summary; exit `0` | Failed inspection is folded into the successful-scan denominator |

The code also treats identical call syntax as self-comparison despite possible side effects, suppresses some candidates using markers that cannot establish assertion authority, and cannot perform the mock-return dataflow implied by its description. Its detector-index documentation and unused helper need reconciliation. Prefer shrinking semantic claims over expanding an ad hoc analyzer. Add behavioral regressions covering missed inspection and legitimate test shapes, with explicit counts for parsed files and inspection failures. A clean result must remain candidate absence, never an all-clear. Retire obsolete generated bytecode only by exact owned paths when implementing the revision.

## Prior-art findings

The search frame was an agent procedure that designs and refactors economical, authoritative tests, evaluates individual fault-detection potency, and limits closure claims. Both component mechanisms and close whole-skill alternatives were searched.

| Primary source | Relationship | Reusable mechanism and boundary |
|---|---|---|
| Li and Offutt, [Test Oracle Strategies for Model-based Testing](https://www.albany.edu/faculty/offutt/research/papers/testOracle.pdf) | Component prior art | RIPR separates reaching a fault, creating an incorrect state, propagating it, and observing it through an oracle. Their model-based experiments also challenge the assumption that checking more state or more often necessarily detects more faults; this is not a universal result for every suite. |
| Vera-Pérez et al., [Reneri](https://arxiv.org/abs/1909.04770) | Component prior art and specialized enabler | Diagnoses undetected transformations by missing infection, propagation, or an effective oracle. Useful lineage for explaining why a reached mutation survives; its Java-oriented machinery is not a replacement for whole-apparatus judgment. |
| Google, [Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html) | Component prior art | Tests that duplicate implementation facts impose change cost without necessarily establishing correct behavior. Supports examining whether permitted refactors remain accepted. |
| Google SRE, [Canarying Releases](https://sre.google/workbook/canarying-releases/) | Adjacent analogue | Bounded evaluation informs whether rollout should proceed, with representative exposure and success criteria. An analogue for staged admission, not a statistical justification for an arbitrary two-case gate. |
| Hypothesis, [flaky failures](https://hypothesis.readthedocs.io/en/latest/tutorial/flaky.html) and [replaying failures](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html) | Component prior art | Replay depends on controlled state as well as inputs; persistent examples and explicit regressions have different portability from version-sensitive replay data. |
| NIST, [Combinatorial Testing](https://www.nist.gov/publications/combinatorial-testing) | Component prior art | Structured interaction coverage can reduce a justified matrix. It does not establish that pairwise testing covers arbitrary failures or that a matrix is needed for a basic capability claim. |
| [mattpocock/skills TDD](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) | Narrower procedural predecessor | Behavior-oriented tests through public interfaces and incremental vertical slices. Does not provide Test Forge's suite economics, execution census, and reduction argument. |
| [obra/superpowers TDD](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md) | Narrower procedural predecessor | Observing the intended red result before implementation is useful sensitivity evidence. Its blanket TDD and rewrite prescriptions should not govern an apparatus review. |
| [Trail of Bits mutation-testing](https://github.com/trailofbits/skills/blob/main/plugins/mutation-testing/skills/mutation-testing/SKILL.md) | Specialized enabler | Configures bounded campaigns using supported mutation tools. Compose when appropriate rather than embedding campaign infrastructure in the generic skill. |

The three public skills' actual `SKILL.md` files were read. They were not installed or evaluated in live agent tasks. Existing lineage in [lineage.md](lineage.md) remains relevant; this review does not claim every older link was freshly revalidated.

The novelty claim that does not survive is invention of potency analysis, mutation-based sensitivity, behavior-focused testing, or staged evaluation. The narrow combination of claim authority, failure-preserving seams, execution admission, economics, and bounded reduction was not found as one close replacement in this search. That is a bounded search result, not proof of uniqueness. Proposed build posture: revise the existing skill and compose with specialist tooling; switch to an external procedure if it demonstrably covers these obligations with less machinery.

## Search coverage and limits

Search date: `20260908`. Local scope included the canonical skill shelf, provider adapters, and relevant installed skill/plugin locations. Public scope included primary papers, Google testing/SRE guidance, Hypothesis documentation, NIST, GitHub skill sources, and citation/name chaining from oracle-adequacy and mutation-diagnosis material.

Representative queries and families actually used:

- `software testing reachability infection propagation revealability RIPR test oracle observability`
- `site.sre.google workbook canarying releases success criteria stop experiment`
- `site.testing.googleblog.com test behavior not implementation change detector tests`
- `"SKILL.md" "mutation-testing" "test-driven-development"`, then targeted Trail of Bits and mattpocock searches
- `site.hypothesis.readthedocs.io flaky failures reproduce random seed`
- `site.nist.gov software testing combinatorial interaction testing failure modes`
- `"RIPR" "Offutt" "revealability" Li 2017` and `"Suggestions on Test Suite Improvements" "Reneri" mutation oracle`
- `"SKILL.md" "test potency"` and `"test adequacy" "valid implementations" oracle mutation false positives`
- `"test suite reduction" "mutation" "oracle" "SKILL.md"` and `"test effectiveness" "reachability" "infection" "propagation" refactoring`

The final combination and older-mechanism families supplied corroboration without a new close whole-skill alternative. Search was bounded, not exhaustive; inaccessible private methods, unindexed skills, and live comparative effectiveness remain outside the evidence. A future independent pilot should evaluate whether agents actually use the procedure well, including false positives and effort. Same-context review and deliberately planted examples cannot supply that calibration.
