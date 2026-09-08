---
name: test-forge
description: >-
  Prove software claims with the narrowest test seam that preserves each failure surface, classify what truth the evidence establishes, and verify that the intended tests actually execute. Use whenever writing, adding, running, reviewing, auditing, redteaming, streamlining, or refactoring tests; designing a test strategy or apparatus from first principles; investigating slow, redundant, flaky, skipped, deselected, mock-heavy, or untrustworthy suites; asking what could break and how to test it; or invoking pytest, jest, vitest, go test, cargo test, or another test runner. Routes between a lightweight FORGE path for ordinary test work, AUDIT for diagnosis, and REFORGE for apparatus redesign.
---

# Test Forge

Treat a test suite as a system of proof, not a collection of test functions. Begin from the claim and the failure it must expose; then choose the truth kind, authority, architectural seam, environment, cadence, and falsifier that make the evidence trustworthy.

The governing question is:

> For every in-scope claim, what concrete defect must be observable, and what is the narrowest trustworthy test that would reject it?

Coverage, test count, marker count, realism, and green commands are supporting signals. None establishes that the right behavior was tested or that the intended evidence ran.

## The proof-obligation record

Use this record when designing a consequential test or reasoning about a suite. Keep it mental for obvious local work; write it into a claim-to-evidence map for an audit or refactor.

```text
Claim:
Failure and propagation:
Truth kind and authority:
Narrowest seam preserving that failure:
Environment and cadence:
Measured cost:
Falsifier or negative control:
Execution selector and result:
Remaining proof limit:
```

The fields constrain one another. A test is misplaced when its assertion is authoritative but its seam cannot observe the named failure, or when its seam is realistic but the assertion establishes only liveness.

## Truth kinds

Truth kind describes what the assertion establishes; it does not describe test size, environment, or cost. Read [references/taxonomy.md](references/taxonomy.md) when classifying a suite or choosing between kinds.

| Kind | Establishes | Authority |
|---|---|---|
| **Oracle** | Correctness | Independent reference, specification, hand calculation, analytic result, or independently planted truth |
| **Property** | Soundness across a domain | Invariant or metamorphic relation |
| **Regression** | Stability, not correctness | Prior or captured behavior with stated provenance |
| **Contract** | Interface conformance | Declared API, protocol, schema, or boundary behavior |
| **Smoke** | Liveness | Successful execution only |

Fuzz/robustness, performance, concurrency, security, compatibility, and lifecycle are orthogonal failure surfaces. Name them when applicable; do not force them into the five functional truth kinds.

## The seam law

Choose the **narrowest authoritative seam that preserves the entire named failure**.

- Test pure transformations directly when no boundary participates in the failure.
- Cross an in-process application boundary for middleware, routing, validation, and serialization policy.
- Cross a real socket when transport, client serialization, or connection behavior is the claim.
- Cross a fresh process or installed artifact when import isolation, entry-point discovery, or packaging is the claim.
- Cross the real operating-system or external-service lifecycle only when that boundary can fail independently.

Move outward because a boundary adds a distinct failure surface, not because broader execution feels more realistic. Use a controlled fake for an expensive inner component when the outer boundary is the subject; use the real component when its numerics, side effects, or compatibility are the subject.

## Evidence economics

Maximize unique failure signal per unit of developer attention and execution cost. Cost never licenses weaker evidence, but it determines placement and cadence after the failure surface is preserved.

- Measure setup, call, and teardown separately when possible; a fast assertion can hide expensive fixture or executor cleanup.
- Share immutable expensive setup across compatible claims and batch inputs whose authority is unchanged by batching.
- Synchronize concurrency and timeout tests on observable events or state; sleep only when elapsed time is itself the behavior under test, and release planted blockers before teardown.
- Preserve a costly test when it alone observes a failure surface. Remove a cheaper-looking duplicate only after proving it adds no distinct authority, seam, cadence, negative-control role, or failure path.
- Assign evidence to an edit loop, routine suite, scheduled job, release gate, or explicit manual run according to cost and environmental availability. A test moved out of the routine loop must remain visibly reachable elsewhere.

## The falsifiability law

> An assertion never observed rejecting a relevant false implementation is not yet known to be live.

Use two complementary forms:

- **Claim-specific falsifier:** deliberately break the behavior, boundary, selector, configuration, or workflow named by the claim and confirm the intended check rejects it. Boundary operators, omitted side effects, wrong routing, removed CI selectors, and corrupted manifests can be better mutants than arithmetic changes.
- **Automated mutation testing:** use a harness where its operators and runtime provide high signal, typically on stable computational or branching logic and on diff-scoped release work. Triage equivalent and low-value mutants rather than optimizing a raw mutation score.

An Oracle test also needs an independently derived expected value; killing a mutant proves sensitivity, not correctness. Read [references/oracles.md](references/oracles.md) for differential, metamorphic, planted-truth, and provenance-locked strategies.

## Choose the operating mode

### FORGE — ordinary test work

Use this path for one test, a bounded code change, or simply running an existing suite.

1. Name the observable claim and a representative defect.
2. Choose the truth kind and independent authority the claim requires.
3. Place the test at the narrowest seam that preserves the defect.
4. Run the smallest command that actually selects the evidence; inspect runner configuration when hidden selectors, optional dependencies, or environment gates can change admission.
5. Observe a relevant failure before calling a new consequential assertion trustworthy.
6. State any material proof limit; do not manufacture a suite-wide ledger for routine local work.

### AUDIT — determine whether an apparatus is trustworthy

Read [references/audit.md](references/audit.md). Audit execution before interpreting green results: configuration, collection, selection, skips, deselection, dependencies, CI commands, warnings, timing, and actual cadence. Then map claims and failure surfaces to evidence, inspect assertion honesty, identify gaps, and establish which costs are dominated.

Use `scripts/smell-scan.py` to seed Python candidates, never as an all-clear. It cannot judge oracle provenance, architectural seams, CI reachability, or semantic redundancy.

### REFORGE — redesign or deeply streamline a suite

Read [references/reforge.md](references/reforge.md), [references/taxonomy.md](references/taxonomy.md), and [references/oracles.md](references/oracles.md). Establish the baseline and proof obligations before editing. Consolidate fixtures, relocate evidence to the right seams, eliminate accidental waiting and repeated setup, repair selection, and remove only tests shown to be evidentially dominated.

For a systematic whole-codebase or release-readiness audit, Audit Planes may derive the architectural risk topology first; Test Forge owns translating those risks into executable evidence and refactoring the test apparatus. Do not make an ordinary suite refactor inherit a whole-codebase audit package.

## Reachability is part of truth

A test that exists but is not admitted contributes no evidence.

- Record collected, selected, skipped, deselected, expected-failure, and warning states separately.
- Execute the exact CI or documented command when selection semantics matter. Naming a file may still inherit a default marker exclusion.
- Verify optional dependency groups and environment gates are installed where their evidence is claimed.
- Treat an unexpected skip, deselection, warning, empty collection, or stale generated artifact as a distinct state, not a pass.
- Replace generic “full suite” language with exact evidence-plane commands and explicit proof limits.

## Closure

A test task closes when its scoped claim has authoritative, reachable evidence and a relevant falsifier. An apparatus audit or refactor closes only when:

- every in-scope claim and material failure surface has evidence or an explicit proof gap;
- each test runs at a seam capable of observing its named failure;
- exact routine, scheduled, release, and manual selectors are documented and selection-checked;
- representative false implementations, configurations, or workflows are rejected;
- skips, deselections, warnings, unavailable environments, and external evidence are reported honestly;
- retained expensive tests have a named unique function and removed tests were proven dominated;
- the final result survives the relevant commands without weakening assertions, selectors, or thresholds.

Passing tests are candidate evidence for closure, never closure by themselves.

## Reasoning trace for apparatus changes

For a material refactor, record consequential decisions rather than narrating every edit:

| Choice | Evidence and reasoning | Rejected alternative | Validation |
|---|---|---|---|

Also retain the baseline, final commands and results, adversarial mutations, and proof limits. Write this trace into the repository only when it has continuing operational or review value, or when the user asks for it; otherwise report it conversationally. A ledger that records routine renames and formatting is audit theatre.

## Anti-patterns

Read [antipatterns.md](antipatterns.md) when auditing or reforging. It pairs category collapses with apparatus-level failures such as realism gradients, selector illusions, marker quotas, planted sleeps, and reduction by count.

## Additional resources

- [references/audit.md](references/audit.md) — execution census, evidence census, dominance analysis, and audit output.
- [references/reforge.md](references/reforge.md) — suite redesign, seam placement, cost shaping, reachability repair, and closure.
- [references/taxonomy.md](references/taxonomy.md) — the five truth kinds, orthogonal surfaces, and conditional module heuristics.
- [references/oracles.md](references/oracles.md) — independent oracle construction and falsification.
- [references/lineage.md](references/lineage.md) — prior-art lineage and the method’s novelty boundary.
- [references/final-review.md](references/final-review.md) — maintenance consultation, reproduced helper defects, and pending revision recommendations; not operative instructions.
- [examples/audit-example.md](examples/audit-example.md) — execution-first audit example.
- [examples/refactor-example.md](examples/refactor-example.md) — proof-obligation-driven apparatus refactor.
- `scripts/smell-scan.py` — Python AST heuristic that emits review candidates, not verdicts.
