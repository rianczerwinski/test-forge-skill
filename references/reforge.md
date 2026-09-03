# REFORGE — redesign or deeply streamline a test apparatus

Reforge toward a smaller, clearer system of proof without trading away fault detection. Begin from an audited baseline; change test placement, fixture topology, execution cadence, and selectors only after naming which evidence survives.

## 1. Establish the invariant

The target is not “fewer tests” or “faster CI.” It is:

> Every in-scope claim has reachable, falsifiable evidence at the narrowest seam that preserves its material failures, and every retained cost buys a named unique signal.

Keep production behavior fixed unless the authorized task includes fixing defects discovered during the refactor. A broken baseline test may expose a test defect or a production defect; distinguish them before editing either.

## 2. Build the claim-to-evidence map

Populate the proof-obligation record from `SKILL.md` for public behavior, numeric truth, state transitions, trust boundaries, compatibility, packaging, concurrency, and lifecycle. Group obligations by shared authority and setup only after they are explicit.

Use source modules as navigation and derive completeness from the claim population; one test file per source file, one marker of each kind, or a coverage threshold cannot supply that denominator.

## 3. Place evidence on the seam ladder

Walk outward only until the named failure becomes observable:

1. pure function or object;
2. in-process subsystem or application;
3. thread/process boundary;
4. local socket or IPC transport;
5. built or installed artifact in a fresh consumer;
6. real dependency or external compatibility surface;
7. operating-system deployment and lifecycle;
8. complete user journey.

This is not a hierarchy of truth. Each rung exists for failures introduced there. Keep at most the broader evidence needed for each independently fallible boundary; do not replay the entire lower-level edge-case matrix on every outer rung.

### Doubles

Replace a component when its behavior is not the claim and the double preserves the inputs and outputs needed to observe the subject. Prefer deterministic, intentionally limited fakes whose proof limits are stated.

Examples:

- Real HTTP application + fake model for validation, middleware, schema, and counter claims.
- Real socket + fake server core for client serialization and connection behavior.
- Real tokenizer + substituted neural forward for an admission boundary decided before inference.
- Real model or independent reference for numeric, semantic, and compatibility claims about that model.

A real inner component can add cost without authority; a fake boundary can erase the failure. Decide from the obligation, not from a blanket preference for mocks or realism.

## 4. Shape the economics

Measure before changing. Preserve baseline counts, selectors, and cold/warm timing when initialization is material.

- Hoist repeated deterministic setup to the narrowest shared fixture lifetime that preserves isolation.
- Share immutable model, compiler, container, database, or artifact acquisition across compatible tests.
- Batch independent inputs through one expensive forward pass when batching does not alter the claim.
- Keep assertion failures diagnostic even when setup is shared; a batch may compute once and expose several precise assertions.
- Replace sleep-based synchronization with events, barriers, fake clocks, or observable state. Release planted blockers before fixture teardown.
- Bind sockets before starting servers and pass the bound socket when the framework supports it; discovering an unused port and binding later creates a race.
- Preserve the isolation actually required: a fresh interpreter may prove import independence without a new virtual environment and package-manager startup; a package-manager claim still requires the package manager.
- Treat warnings as transition signals. Resolve a declared dependency migration rather than globally suppressing it.

Measure the same commands after each coherent cluster. Runtime improvement does not compensate for lost evidence.

## 5. Consolidate without erasing distinctions

Hoist equivalent fixtures and parameterize repeated cases when their authority and seam are identical. Merge assertions that can share an expensive setup without hiding which claim failed.

Delete a candidate only after applying the dominance criteria in [audit.md](audit.md). In particular:

- A real-model copy does not dominate a deterministic protocol test merely because it is broader.
- A unit test does not replace a socket, installed-artifact, or lifecycle test when the boundary itself can fail.
- Coverage equivalence does not establish fault-detection equivalence.
- A negative control can look duplicative while proving the positive oracle is live.

Organize surviving tests by durable ownership. Source mirroring is one option; contract, compatibility, lifecycle, or cross-cutting property homes may be clearer. Dissolve episode-named files once their live evidence has a canonical owner.

## 6. Repair execution reachability

Define explicit evidence planes such as routine, scheduled, release, platform-specific, and manual. For each plane record:

- exact command;
- dependency group and acquired artifacts;
- environment/platform requirements;
- expected collection and selection behavior;
- claims discharged;
- expected cadence and approximate cost.

Selection-check every nonroutine command. A named file can still be excluded by default marker expressions, environment gates, or plugin configuration. Add regression checks around critical workflow selectors when a future edit could silently turn proof into acquisition-plus-deselection.

Do not call unavailable evidence passed. Report where it will run and what remains unproven locally.

## 7. Attack the rebuilt apparatus

Choose representative false mutations from the claims, not merely from available mutation operators:

- flip inclusive/exclusive boundaries;
- delete a required side effect;
- route to the wrong collaborator;
- substitute a circular expected value;
- remove a workflow selector or dependency installation;
- corrupt an artifact identity or manifest;
- bypass the architectural boundary a compatibility test claims to cross;
- disable the mechanism whose accuracy or convergence is asserted.

Confirm the intended test or apparatus check rejects each mutation, then restore the exact source/configuration. Automated mutation tools complement this pass where they provide stable operators and acceptable cost.

Mutation proves sensitivity. Independently inspect expected-value provenance and specifications to establish correctness.

## 8. Preserve the reasoning that matters

For consequential apparatus choices, maintain:

| Choice | Evidence and reasoning | Rejected alternative | Validation |
|---|---|---|---|

Record the baseline, before/after timings, exact commands, mutations, and proof limits. Keep the trace in an ADR or test-apparatus document when it will guide maintenance or review. Omit mechanical edits whose rationale is already obvious from the governing choice.

## 9. Close

Run the routine plane and every affordable affected explicit plane. Selection-check unavailable platform or scheduled planes and disclose that execution limit. Re-run smell heuristics as supporting evidence, inspect the final diff for weakened assertions/selectors, and ensure no production behavior changed unintentionally.

The refactor is complete only when the closure conditions in `SKILL.md` hold. A lower test count, faster command, clean scanner, or green routine run is never sufficient alone.
