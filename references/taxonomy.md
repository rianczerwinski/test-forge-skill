# Truth-kind vocabulary

Truth kind answers one question inside a proof obligation: **what can this assertion legitimately establish?** It does not answer which architectural seam to cross, how realistic the fixture should be, how often the test should run, or whether the test is selected in CI.

## Table of contents

1. The five functional kinds
2. Orthogonal failure surfaces
3. Module-character heuristics
4. Classification discipline
5. Test-tree structure

## 1. The five functional kinds

### Oracle — correctness

An Oracle test compares behavior with an independent source of truth. Independence is load-bearing: if expected and actual derive from the same production mechanism, the comparison is self-consistency or regression, not correctness.

Legitimate authorities include:

- a reference implementation whose relevant mechanism is independently maintained;
- an explicit specification or protocol example;
- a hand-computed value;
- an analytic closed form;
- ground truth planted by an independent generator;
- a metamorphic relation whose transformation is known independently of the implementation.

Read [oracles.md](oracles.md) when independence, provenance, tolerance, or reference cost is nontrivial.

### Property — soundness across a domain

A Property test asserts an invariant over examples or generated inputs: symmetry, monotonicity, idempotence, conservation, permutation invariance, boundedness, or round-trip relations. It need not know the exact answer.

Properties and Oracles complement one another. An implementation can satisfy useful invariants while returning wrong absolute values, and an example oracle can miss a broad input class.

### Regression — stability

A Regression test pins prior behavior and detects change. It does not prove that behavior was correct.

Distinguish:

- **verified-baseline regression:** the pinned behavior was independently validated at capture time;
- **accept-current snapshot:** the output was captured without independent validation.

Record provenance so a future maintainer does not promote a snapshot into an Oracle by implication.

### Contract — interface conformance

A Contract test checks an API, schema, protocol, exception, serialization form, routing decision, CLI status, or boundary interaction. Contract evidence can legitimately use a test double when the observable claim is which collaborator was invoked with which payload.

Asserting that a mock returned its configured value is not Contract evidence. Asserting that the system routed to the mock correctly is.

### Smoke — liveness

A Smoke test proves that representative execution completes, imports, starts, or returns something. Liveness is useful for installations, entry points, and broad paths. It becomes misleading only when its name or surrounding claim implies correctness, accuracy, compatibility, or completeness.

## 2. Orthogonal failure surfaces

The five kinds describe functional truth. Record additional dimensions when the risk lives elsewhere:

- **Fuzz/robustness:** malformed, hostile, or unexpectedly structured inputs.
- **Performance:** latency, throughput, resource, or complexity budgets.
- **Concurrency:** interleavings, races, atomicity, cancellation, and ownership.
- **Security:** adversarial capability and boundary enforcement.
- **Compatibility:** behavior against an actual client, dependency, platform, or version.
- **Lifecycle:** installation, startup, recovery, upgrade, idle, shutdown, and removal.

A test can be Contract + compatibility, Property + concurrency, or Oracle + performance. Record both dimensions; an orthogonal label does not replace the functional kind.

## 3. Module-character heuristics

Use module character to prompt missing proof obligations, not to impose marker quotas.

| Module character | Questions that must be answered |
|---|---|
| Numeric or algorithmic core | What establishes exact or bounded correctness? Which invariants span the input domain? What false mechanism makes the oracle degrade? |
| Stateful logic | Which state invariants, transitions, invalid transitions, retries, and recovery paths matter? Is any converged value independently knowable? |
| IO, storage, protocol, serialization | Which declared contracts and round trips matter? What corruption, partial failure, version mismatch, or trust boundary can propagate? |
| CLI and integration | Which exit, wiring, process, environment, and handoff failures require a broader seam? |
| Pure glue, dispatch, routing | Which collaborator, payload, ordering, and rejection decision is the public behavior? |

An Oracle + Property expectation remains a strong heuristic for numeric cores, and Contract + Smoke often fits IO. Treat those as diagnostic prompts. A mechanical “module has marker X” gate can be satisfied by irrelevant or inert tests and should not issue assurance without an explicit, validated module-to-claim mapping.

When no independent Oracle is currently obtainable, record an oracle gap with the missing authority and best available evidence. A visible gap is stronger than a circular golden labeled Oracle.

## 4. Classification discipline

- Classify the strongest claim each assertion actually supports, not the test name or decorator.
- Let one test carry multiple kinds only when distinct assertions truly establish them.
- Use markers when they improve selection or discoverability in that project; do not make marker presence the evidence.
- Pair every consequential correctness or convergence claim with a falsifier that demonstrates sensitivity.
- Keep expected-value provenance adjacent to the test or fixture when it could otherwise be mistaken for independent truth.

The recurring category-collapse smells are worked in [../antipatterns.md](../antipatterns.md): circular goldens, guarded no-op tests, tautologies, decorative tolerances, mock shadows, static greps posing as behavior, and Oracle names on Smoke assertions.

## 5. Test-tree structure

Organize for ownership and discoverability. Source mirroring is useful when a source module is the natural owner; contract-, lifecycle-, compatibility-, or property-oriented suites may have better cross-cutting homes.

Preserve stable paths unless movement improves maintenance or removes sediment. Dissolve episode-named files such as `test_wave1_rewrite.py` or `test_release_redteam_b7.py` by moving their live evidence to the enduring subsystem or claim owner. Delete the emptied shell after verifying no unique evidence or fixture role remains.

A claim-to-evidence map can provide navigation without forcing every test into one universal directory scheme.
