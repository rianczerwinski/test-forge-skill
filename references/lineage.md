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

Rothermel et al.’s [empirical test-suite reduction studies](https://doi.org/10.1002/stvr.256) found that reduction can severely compromise fault detection even when conventional coverage obligations remain satisfied. Test Forge therefore requires a bounded evidence-preservation argument before deletion. Falsification supports that argument; coverage equivalence, mutant kills, or a lower count cannot supply it alone.

## Oracles and mutation

Barr et al.’s [test-oracle survey](https://doi.org/10.1109/TSE.2014.2372785) supplies the specified, derived, and implicit oracle lineage. Differential testing, metamorphic testing, independently generated fixtures, and provenance-locked references are established responses to the oracle problem.

Public agent skills provide narrower adjacent workflows. The [`mutation-testing` skill](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/mutation-testing/SKILL.md) emphasizes harness-driven, diff-scoped mutation at a PR-readiness cadence. [`adversarial-mutation-test`](https://github.com/rainlanguage/adversarial-mutation-test/blob/main/skills/adversarial-mutation-test/SKILL.md) runs durable behavior-by-behavior mutation campaigns. [`constraint-driven-development`](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md) places measurable quality constraints at lifecycle-appropriate gates.

Test Forge does not duplicate those exhaustive mutation or general quality-bar workflows. It uses claim-specific falsifiers inside a broader method for designing and maintaining test evidence.

## Local composition boundary

The local `audit-planes` skill owns census-backed, whole-codebase assurance and architectural risk topology. Test Forge owns the test apparatus: translating scoped claims and risks into authoritative, reachable, economical, falsifiable evidence. A whole-codebase audit may feed Test Forge; an ordinary test refactor does not require an Audit Planes outpost.

Redteam owns bounded adversarial review under actual operating conditions; Repo Refiner owns physical structure and navigation; Closeout owns unresolved-work capture and commit sequencing; Skill-skill owns canonical authoring and provider discovery. These are conditional composition boundaries, not mandatory dependency chains for routine tests.

## Distinct synthesis

The combination not found as one close replacement in the bounded search below is:

1. truth-kind honesty and oracle independence;
2. claim- and propagation-derived proof obligations;
3. narrowest-failure-preserving seam selection;
4. execution reachability across local, CI, scheduled, release, and platform planes;
5. evidence economics without coverage-based deletion;
6. claim-specific falsification across source, configuration, selectors, artifacts, and workflows;
7. explicit proof limits as part of closure.

The build posture is therefore **resynthesize the existing Test Forge**, compose with Audit Planes for upstream systemic risk census, and leave specialized exhaustive mutation campaigns to dedicated tooling.

## Potency and permitted change

Li and Offutt's [Test Oracle Strategies for Model-based Testing](https://www.albany.edu/faculty/offutt/research/papers/testOracle.pdf) extends RIP to RIPR: reaching a fault, producing an incorrect state, propagating it, and revealing it through an oracle. Its model-based experiments also challenge the assumption that checking more state or checking it more often necessarily detects more faults. This is component prior art; the experimental findings are not universal laws for every suite.

Vera-Pérez et al.'s [Reneri](https://arxiv.org/abs/1909.04770) investigates undetected transformations through infection, propagation, and oracle observations. It supplies a diagnostic precedent for surviving mutants; its specialized machinery does not replace architecture and requirement judgment.

Google's [Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html) explains the maintenance cost of tests that duplicate implementation facts without establishing useful behavior. Test Forge combines this concern with fault sensitivity by checking both rejected defects and accepted valid alternatives.

## Decision-relevant experiments and unreliable evidence

Google SRE's [Canarying Releases](https://sre.google/workbook/canarying-releases/) is an adjacent analogue: bounded evaluation, representative exposure, and success criteria inform whether rollout proceeds. This supports staged decision-making, not a prescribed sample count for a capability experiment.

NIST's [Combinatorial Testing](https://www.nist.gov/publications/combinatorial-testing) supplies methods for economical interaction coverage where a matrix is justified. It does not make a matrix obligatory or make pairwise coverage sufficient for arbitrary failure families.

Hypothesis' [flaky-failure guidance](https://hypothesis.readthedocs.io/en/latest/tutorial/flaky.html) and [replay guidance](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html) distinguish controlled examples from uncontrolled state and version-sensitive replay data. They support preserving initial failures and sufficient input/environment/history context instead of treating retries or seeds as universal resolution.

## Closest public skills

| Inspected source | Relationship and reuse boundary |
|---|---|
| [mattpocock TDD](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) | Narrower procedural predecessor: behavior/public interfaces and vertical slices. Reuse the behavior focus; apparatus economics, execution admission, and reduction need additional work. |
| [obra/superpowers TDD](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md) | Narrower procedural predecessor: observe the intended red result. Its blanket TDD/rewrite prescriptions do not govern suite audits. |
| [Trail of Bits mutation-testing](https://github.com/trailofbits/skills/blob/main/plugins/mutation-testing/skills/mutation-testing/SKILL.md) | Specialized enabler for bounded supported mutation campaigns. Compose when relevant instead of growing campaign infrastructure into the generic skill. |

These actual SKILL.md files were inspected in the search; they were not installed or empirically compared in live tasks. Potency analysis, behavior-based testing, mutation sensitivity, and staged evaluation are established methods. The bounded search supports the synthesis posture, not an invention or uniqueness claim.

## Search record and limits

Search date: `20260908`. The search covered canonical/provider skill locations, relevant installed plugin locations, primary papers, Google testing/SRE guidance, Hypothesis, NIST, and public GitHub skills. Citation/name chaining connected oracle-adequacy and mutation-diagnosis sources. Earlier lineage remains recorded above; not every older link was freshly revalidated.

Representative query families:

- `software testing reachability infection propagation revealability RIPR test oracle observability`
- `site.sre.google workbook canarying releases success criteria stop experiment`
- `site.testing.googleblog.com test behavior not implementation change detector tests`
- `"SKILL.md" "mutation-testing" "test-driven-development"`, followed by Trail of Bits and mattpocock source searches
- `site.hypothesis.readthedocs.io flaky failures reproduce random seed`
- `site.nist.gov software testing combinatorial interaction testing failure modes`
- `"RIPR" "Offutt" "revealability" Li 2017` and `"Suggestions on Test Suite Improvements" "Reneri" mutation oracle`
- `"SKILL.md" "test potency"` and `"test adequacy" "valid implementations" oracle mutation false positives`
- `"test suite reduction" "mutation" "oracle" "SKILL.md"` and `"test effectiveness" "reachability" "infection" "propagation" refactoring`

The final two combination/ancestral families added corroboration without a new close whole-skill alternative. Private methods, unindexed skills, and comparative live effectiveness remain outside the evidence. Reconsider the synthesis if a demonstrated alternative covers its obligations with less machinery.
