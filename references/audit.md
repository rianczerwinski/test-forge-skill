# AUDIT — assess a test apparatus

Diagnose the requested apparatus without changing it unless implementation is authorized. Use the decision/claim record in SKILL.md rather than maintaining a second schema.

## Scope and affordable baseline

Bind the revision and preserve user changes. Read runner configuration, test documentation, dependency groups, and relevant workflows before running commands. Establish the decision and scope before interpreting the current suite as the obligation population. Apply the decision-before-cost gate before expensive acquisition or baseline runs.

Record exact applicable commands, environmental gates, collection/selection/result states, warnings, and cost evidence. Use cold/warm timings and setup/call/teardown attribution when initialization matters. Missing optional dependencies are unavailable evidence; install only within authority.

A cheap collection pass can expose hidden default selectors before expensive setup. Collection is not execution, and naming a file does not override every runner default.

## Derive the obligation population

Read claims from owner requirements, specifications, public behavior, architecture, state transitions, incident history, compatibility promises, and deployment commitments. Label inferred risks and historical baselines distinctly. State the bounds, assumptions, and uninspected areas.

Trace material failures through the actual boundaries and histories. Include shared fixtures, configuration, generated inputs, and CI selectors where they can invalidate many tests. Explore interacting conditions when there is a causal reason for interaction; neither all combinations nor pairwise combinations are universal defaults.

Consume Audit Planes' risk topology when the requested conclusion is whole-system assurance. Keep a bounded apparatus audit scoped to its evidence questions.

## Evaluate individual potency

Apply [potency.md](potency.md) to consequential evidence: validate the setup, trace activation/propagation/observation, inspect authority, and challenge both missed faults and rejected valid behavior. Use [taxonomy.md](taxonomy.md) to describe what the assertions support.

The Python scanner can seed a small candidate list. Check its parsed-file, test-function, and error counts before using the result; its population is syntactic, not the runner's admitted tests. Manually inspect high-consequence tests and unsupported patterns regardless of candidate count.

Prioritize findings that create false confidence: relevant faults surviving tests; unique evidence never selected; circular expectations or bypassed boundaries; flaky/unavailable evidence; then waste. Each finding names location, claim, delivered evidence, consequence, validation, and proposed disposition.

## Seams and doubles

Determine which independently fallible boundaries each claim requires. Real HTTP policy with a fake model can establish admission behavior; it cannot establish the model's numerical quality. A socket test observes transport that an in-process client bypasses.

Check a double's conformance only to the extent that the conclusion relies on it faithfully representing a dependency. Returning a collaborator's configured value can legitimately test a wrapper's pass-through contract. Confirm which component's behavior was exercised before calling it a mock shadow.

## Flaky evidence

Keep the first attempt and distinguish later retry outcomes. Retain the input, minimized example where available, random seed, dependency/platform identity, prior state/order, and relevant timing. A seed alone cannot reconstruct external state or scheduling.

Separate product races from harness faults, fixture leakage, order dependence, resource contention, and clock dependence. Quarantine preserves visibility with a named owner/follow-up and an exit condition; exclude its claim from passed evidence until the required execution is reliable. A retry success does not erase the original failure.

## Bounded evidential dominance

Delete as redundant only with an argument that surviving reachable evidence supports the same claim with equal or stronger relevant authority, preserves the candidate's material failure paths, and retains required cadence, platform, compatibility, negative-control, and diagnostic roles.

State the argument's fault families, inputs, state histories, and environmental bounds. Equal coverage, broader execution, and representative mutant kills alone cannot prove universal equivalence. Use mutants as supporting probes. If a material unique role remains uncertain, retain the evidence until a replacement demonstrates preservation of that role. Earlier removal requires explicit owner authorization to accept the named evidence gap; record that authorization and the outstanding obligation, not a claim of redundancy or readiness. Recording an obligation alone does not authorize deletion.

Retiring a requirement is a different act from removing duplicate evidence. Cite owner authority for a requirement's retirement; a cheaper apparatus does not authorize changing what the product promises.

## Attribute cost and execution gaps

Separate essential costs from repeated setup, unnecessary forwards, arbitrary sleeps, blocked teardown, racy port discovery, irrelevant environment creation, and duplicated matrices. State evidence preserved alongside estimated savings.

Inspect exact selectors, dependencies, workflow steps, and fixture identities on applicable routine/scheduled/release/platform/manual paths. Check the consumer's expected generated-input revision; refresh only if authorized, preserving user-specified snapshots.

## Deliver

Return the bounded baseline, significance-first findings, claim-to-evidence map, justified consolidation candidates, and dependency-ordered proposed repairs. Report denominators and uncertainty for any reduction estimate.

An audit can complete with identified gaps and unimplemented repairs. Call the diagnosis complete only for its assessed scope; state separately whether any readiness or implementation claim remains unsupported.
