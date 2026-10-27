---
name: test-forge
description: >-
  Calibrate, build, and refine software and workflow failure-detection machinery around real consequences, valid criteria, potent checks, and minimum total burden. Use when writing, running, reviewing, or refactoring tests or validators; designing assurance or closure checks; investigating slow, redundant, flaky, skipped, mock-heavy, or untrustworthy suites; asking whether assurance is enough or overbuilt, how serious an engineering failure is, when to stop testing, or whether a check detects real faults; or invoking pytest, jest, vitest, go test, cargo test, or another test runner. Use CALIBRATE to reground scope and rigor, FORGE for bounded test work, AUDIT for apparatus diagnosis, and REFORGE for redesign. Route whole-system assurance to Audit Planes.
license: MIT
---

# Test Forge

Build the least burdensome trustworthy apparatus that answers the actual decision, fully addressing its scoped obligations. Optimize technical assurance and the experience of using and maintaining it together: runtime, false alarms, coordination, and ceremony are part of the design. Fewer checks or more rigor alone is not success. Connect each claim to its source, material failures, authority, failure-preserving seam, effective assertion, and execution evidence. Counts, coverage, realism, and green commands are supporting observations, not substitutes for that argument.

## Choose the operating mode

- **CALIBRATE:** answer “how serious is this, and what assurance earns its place?” Read [references/calibration.md](references/calibration.md). Locate the decision, consequences, missing evidence, and useful stopping point. Return a bounded disposition; build nothing unless authorized. This is independently callable, including mid-task.
- **FORGE:** write or change a bounded set of tests or executable checks, or run an existing suite. Apply the calibration below briefly, then follow the changed-tests procedure. For a run-only request, inspect the relevant command and gates, execute within authority and cost limits, and report the actual results. An unchanged routine run does not require a new claim map or mutation campaign.
- **AUDIT:** diagnose whether the test apparatus supports its claims. Read [references/audit.md](references/audit.md), [references/potency.md](references/potency.md), and [antipatterns.md](antipatterns.md). Return findings and proposed changes; implement only when authorized.
- **REFORGE:** deeply streamline or redesign the apparatus. Read [references/reforge.md](references/reforge.md), [references/potency.md](references/potency.md), [references/taxonomy.md](references/taxonomy.md), [references/oracles.md](references/oracles.md), and [antipatterns.md](antipatterns.md). Preserve the claims while improving evidence placement, execution, and cost.

Apply the same method to validators, migration checks, and executable evidence or closure checks when they support a consequential decision. Test Forge owns their assurance design, not the surrounding migration or workflow. For whole-codebase or release-readiness assurance, use Audit Planes for the upstream risk population; Test Forge translates it into test evidence. Redteam owns bounded adversarial review, Recompass owns broader direction and governing-assumption assessment, Repo Refiner owns physical organization/navigation, and Closeout owns unresolved-work capture. Use those capabilities only when that work is in scope; ordinary testing does not inherit their full procedures.

## Calibrate before adding machinery

Ground rigor in the actual operation and failure, not the project's category or the agent's confidence. An audio utility can contain both a reversible display bug and loss of irreplaceable recordings. Trace plausible accidental engineering failures first; include hostile actors when the operating environment or explicit threat model makes them relevant. Deliberately wrong fixtures simulate faults; they do not imply malicious users.

Check both directions: which material failure could pass unnoticed, and which control adds no distinct protection or wrongly rejects valid behavior? Consider consequence, exposure, propagation, visibility, recoverability, uncertainty, and existing controls. Keep these dimensions visible; avoid invented probability scores or a universal number of assurance layers.

Prefer removing a failure opportunity through a simpler design, type, transaction, or boundary check when that improves both assurance and usability. Otherwise choose the smallest evidence path that preserves the failure. Additional machinery must address a named material doubt with evidence capable of changing the decision or preserving a necessary guarantee. Include its maintenance, false-rejection, coordination, and failure costs, not just execution time. Retain useful prevention and regression protection even when recent finding yield is zero.

For a routine local change, a sentence and the relevant check can settle this. Read [references/calibration.md](references/calibration.md) when the scale is disputed, assurance is being designed, the decision is consequential, or findings change the assumptions. Preserve the stronger route when it materially improves the outcome; remove incidental friction instead of silently weakening the guarantee. Honor applicable owner and repository closure requirements; calibration selects an economical way to meet them, not an implicit waiver.

## Start with the decision and claim

Ask what result would change the next action. Distinguish a capability demonstration, regression check, boundary guarantee, and reliability estimate over a population.

Use this record for consequential new evidence or apparatus work. Keep obvious local reasoning brief; write a claim-to-evidence map when the scope or requested trace warrants it.

```text
Decision and pass/fail/inconclusive actions:
Claim, source, and status (specified / inferred / historical); criterion validity:
Scope, assumptions, and excluded claims:
Consequence, visibility/recovery, existing protection, and protected qualities:
Failure path, including relevant states and interactions:
Truth kind and expected-value authority:
Narrowest seam preserving that failure:
Setup validity, rejected defect, and permitted alternatives:
Execution command, environment, and cadence:
Total burden and distinct evidence gained; stop/expansion condition if nonroutine:
Actual selection/result and falsifier outcome:
Proof limit or unresolved obligation:
```

Derive the failure population from the actual architecture and commitments, not from the existing tests or one-test-file-per-module conventions. Use boundary and state paths to identify relevant omission, corruption, duplication, ordering, timing, partial persistence, stale identity, access, and recovery failures. Apply these as prompts where they participate causally; avoid a compulsory Cartesian checklist. Include shared fixtures, configuration, workflows, and state histories when selecting affected evidence.

Separate observed behavior, inferred intent, and explicit owner commitments. Check that the criterion measures the intended outcome in actual use; alignment with existing behavior alone establishes neither correctness nor deliberate choice. Keep comparison criteria stable across candidates. Report a justified criterion change separately and reassess affected evidence; do not manufacture progress by moving the target. Name protected qualities so aggregate improvements cannot hide their deterioration. A complete map of scoped obligations supports a bounded conclusion; it cannot enumerate every possible failure of arbitrary software.

## Decide before paying

Before costly acquisition, an expensive baseline, or a matrix launch, establish:

- the first informative batch, its chosen conditions, and what it can and cannot establish;
- pass, fail, and inconclusive actions, including a stopping or expansion condition;
- available cost evidence, then a bounded throughput sample if measurement is needed;
- projected setup, execution, teardown, resource cost, and an authorized bound;
- overlap with later stages and reuse bound to compatible code, configuration, inputs, and evidence identities.

Estimate before measuring when measurement itself is expensive. Enforce declared budgets, selectors, and admission conditions in existing runner/job mechanisms where feasible. Human judgment supplies which experiment is informative; a generic validator cannot infer that from a filled-out template. If cost or sampling assumptions fail, revise the next batch before expanding. A two-case gate is no more universal than a full survey. A budget can stop execution with an inconclusive result; it cannot turn missing evidence into a pass. For statistical claims, use a sampling and stopping design that supports the claimed error bounds.

## Place and classify the evidence

Choose the **narrowest authoritative seam that preserves the entire named failure**. Select boundaries by their independent failure surfaces: pure computation; in-process application policy; threads/processes; sockets/IPC; built artifacts; real dependencies; operating-system lifecycle; user journeys. These are choices, not a fixed realism ladder.

Substitute expensive components outside the claim when their doubles preserve its failure conditions. When a conclusion depends on a double representing a real dependency, check the relevant conformance and assumptions. A routing stub need not earn the authority of a full dependency emulator.

For an operational promise, include the actual entry path and configuration where assembly can fail; passing component checks alone cannot establish that path. Assess independence by source, assumptions, mechanism, and observation. Another model or repeated review is not automatically another independent authority; target what the existing evidence could share or miss.

Truth kinds describe assertions, independently of size or cadence. Read [references/taxonomy.md](references/taxonomy.md) for classification and [references/oracles.md](references/oracles.md) for nontrivial oracle choices.

| Kind | Evidence supports | Authority |
|---|---|---|
| Oracle | Correctness for exercised cases under stated assumptions | Independent reference, specification, calculation, or planted truth |
| Property | An invariant/relation on exercised inputs | Independently justified invariant or relation |
| Regression | Stability against a named baseline | Prior behavior with capture/validation provenance |
| Contract | Declared boundary behavior | API, protocol, schema, or interaction commitment |
| Smoke | Successful representative execution | Observed startup, import, or completion |

Record fuzz/robustness, performance, concurrency, security, compatibility, and lifecycle as additional risk dimensions. Neither a marker nor a truth-kind label guarantees adequacy.

## Explicit potency check

For a new or materially changed consequential assertion, engage this question directly: **does it reject the relevant wrong behavior while accepting permitted behavior?**

Trace setup → fault reached → incorrect state → propagation → observed rejection. Verify the setup actually activates the intended conditions, and inspect tolerances, ordering, identity, nondeterminism, and doubles for accidental exclusion of correct alternatives. Read [references/potency.md](references/potency.md) for the shared procedure, including safe falsification and outcome triage.

A relevant observed pre-fix failure can establish sensitivity. Otherwise use a targeted isolated falsifier; use automated mutation campaigns when their additional signal justifies the cost. A mutation killed by an unrelated import failure supplies no behavioral evidence. Sensitivity, oracle authority, and the scope of fault coverage are separate questions.

## FORGE for changed tests

1. Calibrate the decision and consequence; name the scoped claim, valid criterion, authority, and a representative defect.
2. Choose the failure-preserving seam and valid setup.
3. Design the assertion to reject that defect and accept permitted alternatives; apply the potency check in proportion to consequence.
4. Run the smallest command selecting the affected evidence, including shared-fixture/configuration impact.
5. Inspect the actual result and material proof limits. Preserve relevant failing evidence before repairing it.

Keep ordinary work conversational unless a durable trace is requested or has continuing maintenance value.

## Execution and economics

- Record collection, selection, pass, failure, skip, deselection, expected failure, warnings, and unavailable environments distinctly. Naming a file may still inherit a default exclusion.
- Run exact documented/CI selectors where admission matters; verify required dependencies and generated-input identities before crediting their evidence. Report unavailable evidence without installing or refreshing anything beyond the task's authority.
- Retain the first failure and report retries separately. Use input, seed, order/history, environment, and timing evidence to distinguish product failures from harness instability. Quarantine has an owner and exit condition and remains a proof gap.
- Measure setup, call, and teardown when cost matters. Share immutable setup and batch compatible work without changing the claim or hiding diagnostic detail.
- Synchronize on events/state, or on time when elapsed time is the subject. Release planted blockers before teardown.
- Retain expensive evidence with a unique role; move it to a reachable cadence when appropriate. Delete only with the bounded dominance argument in the audit reference.

Use `scripts/smell-scan.py` only to seed Python review candidates. It reports inspection failures separately and exits `2` for incomplete inspection or no named tests. Exit `0` means inspection completed, with or without candidates; its function count is not runner collection. Review semantics, authority, seams, and selection independently.

## Closure and reasoning

- **Diagnosis complete:** the requested population has been assessed; findings, uninspected areas, and proof gaps have explicit dispositions. This does not imply that repairs or system readiness are complete.
- **Implementation complete:** the authorized changes preserve the scoped obligations, pass the affected reachable checks, and survive relevant falsification. Unavailable required evidence limits the completion claim; report the precise remaining obligation.
- **Readiness established:** the independently sourced readiness obligations are discharged at the required environments and cadence. A captured gap is preserved, not discharged.

For a consequential refactor, retain a compact choice/evidence/rejected-alternative/validation trace, baseline and final commands, deletion arguments, falsifier outcomes, and proof limits. Record claim changes separately from apparatus changes. Mutants designed alongside the tests demonstrate those particular detections; they do not calibrate recall on unseen defects.

Stop adding machinery when required evidence supports the scoped decision and no unresolved material doubt has a justified next check. Stop an uninformative path as inconclusive when appropriate; preserve required missing evidence as an obligation. Recalibrate when a finding reveals a shared cause, assumptions drift, consequences change, or the apparatus itself becomes unreliable. A local fix does not close a demonstrated sibling-failure question. See [references/calibration.md](references/calibration.md) for bounded expansion and retirement.

## Additional resources

- [references/calibration.md](references/calibration.md) — consequence, criterion validity, evidence depth, marginal value, and stopping.
- [references/audit.md](references/audit.md) — population, execution census, potency, flaky evidence, and bounded dominance.
- [references/reforge.md](references/reforge.md) — authorized suite redesign and cost shaping.
- [references/potency.md](references/potency.md) — individual test potency, permitted behavior, and isolated falsification.
- [references/taxonomy.md](references/taxonomy.md) — assertion kinds and orthogonal risks.
- [references/oracles.md](references/oracles.md) — authority, independence, snapshots, and numerical error budgets.
- [references/lineage.md](references/lineage.md) — primary prior art, composition, and search limits.
- [antipatterns.md](antipatterns.md) — paired failure patterns for auditing and reforging.
- [examples/audit-example.md](examples/audit-example.md) — historical execution-first audit.
- [examples/refactor-example.md](examples/refactor-example.md) — historical apparatus refactor.
- [examples/potency-example.md](examples/potency-example.md) — decision gate and speaker-grouping potency.
- [examples/calibration-example.md](examples/calibration-example.md) — contrasting minimal and deeper assurance, including agentic workflow checks.
- [references/final-review.md](references/final-review.md) — revision reasoning and validation record; maintenance only.
- [scripts/smell-scan.py](scripts/smell-scan.py) — Python syntax candidate scanner; run on selected test paths.
- [scripts/test_smell_scan.py](scripts/test_smell_scan.py) — dependency-free helper regressions; run with `python3 -B scripts/test_smell_scan.py` from this skill directory.
