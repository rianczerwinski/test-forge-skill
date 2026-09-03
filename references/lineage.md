# Method lineage and novelty boundary

Test Forge composes established methods. Its value is the operational synthesis, not a claim that the underlying ideas are new.

## Claims and evidence

The [OMG Structured Assurance Case Metamodel](https://www.omg.org/spec/SACM/2.2/PDF) formalizes claims, argumentation, evidence, evidence provenance, and incomplete assurance cases. Test Forge adopts the lightweight claim→evidence discipline but does not require a formal assurance-case model for ordinary software testing.

NASA’s [Requirements Verification Matrix](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/) maps each sourced requirement to a definitive verification approach. Test Forge generalizes that traceability beyond written “shall” requirements to architecture-derived failures, incidents, compatibility promises, and lifecycle claims, while keeping proof limits explicit.

## Test seams, size, and cadence

Google’s [Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html) distinguishes small, medium, and large tests by resources and environmental behavior, making size enforceable rather than impressionistic. Google’s [Hermetic Servers](https://testing.googleblog.com/2012/10/hermetic-servers.html) demonstrates controlled whole-server testing without external network dependence.

The [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) argues for many narrow tests, fewer broad end-to-end tests, and focused integration tests at independently fallible boundaries. Test Forge replaces fixed portfolio proportions with a failure-preserving seam rule: cross exactly the boundaries required by each proof obligation.

## Selection, prioritization, and reduction

Rothermel and Harrold’s [safe regression-test selection work](https://www.cs.purdue.edu/homes/xyzhang/spring07/Papers/p173-rothermel.pdf) treats selection as a correctness problem with explicit conditions, not merely a speed optimization. Elbaum, Malishevsky, and Rothermel’s [test prioritization studies](https://digitalcommons.unl.edu/csearticles/8/) establish cost and early fault detection as legitimate portfolio concerns.

Rothermel et al.’s [empirical test-suite reduction studies](https://doi.org/10.1002/stvr.256) found that reduction can severely compromise fault detection even when conventional coverage obligations remain satisfied. Test Forge therefore requires evidential dominance or falsification evidence before deletion; equivalent coverage or a lower count is insufficient.

## Oracles and mutation

Barr et al.’s [test-oracle survey](https://doi.org/10.1109/TSE.2014.2372785) supplies the specified, derived, and implicit oracle lineage. Differential testing, metamorphic testing, independently generated fixtures, and provenance-locked references are established responses to the oracle problem.

Public agent skills provide narrower adjacent workflows. The [`mutation-testing` skill](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/mutation-testing/SKILL.md) emphasizes harness-driven, diff-scoped mutation at a PR-readiness cadence. [`adversarial-mutation-test`](https://github.com/rainlanguage/adversarial-mutation-test/blob/main/skills/adversarial-mutation-test/SKILL.md) runs durable behavior-by-behavior mutation campaigns. [`constraint-driven-development`](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md) places measurable quality constraints at lifecycle-appropriate gates.

Test Forge does not duplicate those exhaustive mutation or general quality-bar workflows. It uses claim-specific falsifiers inside a broader method for designing and maintaining test evidence.

## Local composition boundary

The local `audit-planes` skill owns census-backed, whole-codebase assurance and architectural risk topology. Test Forge owns the test apparatus: translating scoped claims and risks into authoritative, reachable, economical, falsifiable evidence. A whole-codebase audit may feed Test Forge; an ordinary test refactor does not require an Audit Planes outpost.

## Distinct synthesis

The combination not found as one close skill is:

1. truth-kind honesty and oracle independence;
2. claim- and propagation-derived proof obligations;
3. narrowest-failure-preserving seam selection;
4. execution reachability across local, CI, scheduled, release, and platform planes;
5. evidence economics without coverage-based deletion;
6. claim-specific falsification across source, configuration, selectors, artifacts, and workflows;
7. explicit proof limits as part of closure.

The build posture is therefore **resynthesize the existing Test Forge**, compose with Audit Planes for upstream systemic risk census, and leave specialized exhaustive mutation campaigns to dedicated tooling.
