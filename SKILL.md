---
name: test-forge
description: >-
  Establish what kind of truth each test provides — oracle, property, regression, contract, or smoke — and enforce that every module carries the kinds it needs. Use whenever writing, adding, running, auditing, redteaming, refactoring, or reviewing tests; when asked whether a test suite is trustworthy or how much redundancy / mismeasurement / pointless effort it holds; when designing or restructuring a test suite from first principles; or the moment you are about to invoke a test runner (pytest, jest, go test, cargo test, vitest) or write a new test. Detects category-collapse test smells (circular goldens, can't-fail conditional-guard tests, in-test tautologies, unfalsifiable assertions, mock-shadow tests) and works the test-oracle problem (differential and metamorphic testing, reference oracles, mutation-checked negative controls).
---

# test-forge

A test is not defined by what it covers. It is defined by **what kind of truth it can establish.** Coverage percentage measures nothing; a 38k-line suite at 1:1 test-to-source can be 18% inert. The one question that matters: *for each thing under test, does a test exist that could actually fail if that thing were wrong?*

Every recurring test pathology is a **category collapse** — a test claiming a stronger kind of truth than its assertion can deliver. A smoke test wearing a correctness name. An equivalence check wearing an oracle name. A tautology wearing a property name. This skill names the kinds so the collapse becomes visible, then holds each module to the kind it needs.

## When you reach for this

Two modes, one spine:

- **AUDIT** an existing suite — measure redundancy, mismeasurement, and pointless effort; produce a triaged findings catalog. → read [references/audit.md](references/audit.md).
- **DESIGN / REFACTOR** a suite from first principles — assign required kinds per module, solve the oracle problems, restructure. → read [references/taxonomy.md](references/taxonomy.md) then [references/oracles.md](references/oracles.md).

But the spine applies even to a single test you are about to write in passing. Before writing or running any test, name its kind and confirm its assertion could fail. That habit is the whole skill; the rest is scale.

## The five kinds (the spine)

Ordered by strength of truth. Full treatment in [references/taxonomy.md](references/taxonomy.md).

| Kind | Establishes | Its oracle is… | A legit pass looks like |
|---|---|---|---|
| **Oracle** | Correctness | An *independent* truth: reference implementation, hand-computed value, analytic closed form, or planted ground-truth | numpy op equals the torch output; the estimator recovers the 45° source you planted |
| **Property** | Soundness | A mathematical invariant that must hold for *all* inputs | covariance stays PSD; embeddings stay L2-normed; fused output stays sorted |
| **Regression** | Stability (not correctness) | A committed snapshot of *current* behavior | output equals the golden — **and the test says "detects change, not correctness"** |
| **Contract** | Interface shape | The declared API | raises `FileNotFoundError`; serializes round-trip; routes speaker→text |
| **Smoke** | Liveness | Nothing — it only proves it ran | `assert result is not None` — **fine, when the test name says smoke** |

The kinds map onto established practice, which the skill leans on rather than reinventing: **Oracle** is the *test oracle problem* (oracles classed derived / specified / implicit); a differential oracle (impl-vs-reference) and a metamorphic oracle (relation across inputs) are the two workhorses. **Property** is property-based testing. The **negative-control** law below is the *mutation-testing* premise stated plainly. The audit smells map onto the van Deursen test-smell catalog (Missing Assert / Unknown Test, Assertion Roulette, Mock Overuse).

## The required-kinds rule

A module cannot ship with only the weak kinds. Assign each source module its floor:

| Module character | Required floor |
|---|---|
| Numeric / algorithmic core (model port, DSP estimator, solver, transform) | **Oracle + Property** (+ a negative control) |
| Stateful logic (filter, scheduler, state machine) | **Property + Contract**, Oracle where truth is knowable |
| IO / serialization / protocol / storage | **Contract + Smoke** |
| CLI / cross-module integration | **Contract + Smoke** |
| Pure glue / dispatch / routing | **Contract** |

A numeric module whose only coverage is Smoke has **no correctness coverage** — that is a hole, regardless of how many such tests exist. `scripts/kind-coverage.py` flags these mechanically once tests are marked by kind.

## The negative-control law (kills the can't-fail class)

> **An assertion you have never seen fail is not known to be able to fail.**

This is mutation testing compressed to one sentence. Enforce it two ways:

- **Paired negative control** — for every accuracy or convergence claim, write a sibling test that *breaks the mechanism* and asserts the metric degrades. If disabling the thing under test still passes the test, the test was measuring nothing. (A model of this: a DOA-tolerance test that proves error *explodes* when re-estimation is removed.)
- **Mutation testing** as the systematic backstop on the numeric core only (mutmut, cosmic-ray, Stryker) — flip `+`↔`-`, `<`↔`<=`, and require a test to catch it. This is what catches every conditional-guard and every over-wide tolerance automatically. Do not run it on IO/glue; the payoff is in the math.

## Audit mode, in brief

Run the redteam lens (full detectors, greps, and severity model in [references/audit.md](references/audit.md); `scripts/smell-scan.py` produces file:line candidates for review). The seven category-collapse traps:

1. **Circular golden** — the golden was generated by the code under test. It detects change, never correctness; fatal when its name claims "reference" or "oracle."
2. **Conditional-guard can't-fail** — every assertion sits inside `if <precondition>:`; when the precondition is not met, zero assertions run and the test goes green on exactly the failure it names.
3. **In-test tautology** — the expected value is recomputed by the same code under test, or `assert x == x`.
4. **Weakened-until-unfalsifiable** — tolerance far wider than the quantity's scale, `assert regime in (A, B)` covering N-of-M, or a range check that cannot fail (`0 <= az < 360`).
5. **Mock-shadow** — the assertion checks a mock's own configured return value, or `assert_called_once` is the only signal; nothing real ran.
6. **Static-grep-as-behavior** — a `re.search` over source text dressed as a behavioral test.
7. **Oracle-name-on-smoke** — the name says *localizes / correct / accurate* while the body asserts only `not None` / `len > 0`.

Every finding gets: file:line, kind-claimed vs kind-delivered, severity, and one recommendation (delete / merge / tighten / fix). Prioritize the tests that would stay green through the regression they name — those are more dangerous than redundant ones.

## Design / refactor mode, in brief

The refactor is fundamentally a *taxonomy* refactor, not a rewrite. Sequence (full version in [references/taxonomy.md](references/taxonomy.md)):

0. **Taxonomy in place** — define the five kind-markers and the required-kinds table; gate only *new* tests at first. Stops the bleeding, touches nothing.
1. **Triage sweep** — classify every existing test by kind; delete the dead / tautological / can't-fail; relabel goldens honestly. (This is the audit output, executed.)
2. **Fill oracle gaps** — stand up the independent oracles ([references/oracles.md](references/oracles.md)); every numeric module gets a real oracle + negative control.
3. **Consolidate** — structure mirrors *source*, not development episodes; hoist duplicated fixtures to a shared conftest; dissolve episode-named files (`wave_*`, `*_upgrades`, `redteam_manifest_*`) into subsystem suites under the right marker.
4. **Enforce** — flip the kind-gate to all tests; add mutation testing on the numeric core.

Phases 1 and 3 are cleanup you can start immediately. Phase 2 is the real project and blocks on the oracle decisions — surface those as decision forks, do not pick silently.

## Worked examples

- [examples/audit-example.md](examples/audit-example.md) — a real suite audited into a triaged catalog.
- [examples/refactor-example.md](examples/refactor-example.md) — a suite charted into a first-principles rebuild.

## Anti-patterns

[antipatterns.md](antipatterns.md) — the category collapses as wrong→right pairs, each with the discriminating feature that flips it.
