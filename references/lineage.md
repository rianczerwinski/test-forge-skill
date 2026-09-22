# Method lineage and novelty boundary

Test Forge composes established methods. Its value is the operational synthesis, not a claim that the underlying ideas are new.

## Contents

- [Claims and evidence](#claims-and-evidence)
- [Test seams, size, and cadence](#test-seams-size-and-cadence)
- [Selection, prioritization, and reduction](#selection-prioritization-and-reduction)
- [Oracles and mutation](#oracles-and-mutation)
- [Local composition boundary](#local-composition-boundary)
- [Distinct synthesis](#distinct-synthesis)
- [Potency and permitted change](#potency-and-permitted-change)
- [Decision-relevant experiments and unreliable evidence](#decision-relevant-experiments-and-unreliable-evidence)
- [Closest public skills](#closest-public-skills)
- [Search record and limits](#search-record-and-limits)
- [Python helper implementation](#python-helper-implementation)
- [Assurance calibration](#assurance-calibration)

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

The local `audit-planes` skill owns census-backed, whole-codebase assurance and architectural risk topology. Test Forge owns the assurance apparatus for scoped decisions: calibrating and translating claims and risks into authoritative, reachable, economical, falsifiable checks. This includes test suites and executable validators used by workflows; it does not make Test Forge the owner of those workflows. A whole-codebase audit may feed Test Forge; an ordinary test refactor does not require an Audit Planes outpost.

Redteam owns bounded adversarial review under actual operating conditions; Repo Refiner owns physical structure and navigation; Closeout owns unresolved-work capture and commit sequencing; Skill-skill owns canonical authoring and provider discovery. These are conditional composition boundaries, not mandatory dependency chains for routine tests.

Recompass supplies broader assessment of direction and governing assumptions. Test Forge questions criteria to establish a valid test decision, preserving the distinction between observed behavior, inferred intent, and owner commitments. It does not absorb business strategy, identity work, or the entire Recompass suite. Calibration stays within Test Forge because apparatus design and the judgment of how much apparatus is warranted share the same decision, failure paths, and evidence.

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

## Python helper implementation

The bounded repair review on `20260908` reused the domain and skill-ecosystem reconciliation above and checked Python's primary [source-decoding API](https://docs.python.org/3/library/tokenize.html#tokenize.open) and [AST traversal API](https://docs.python.org/3/library/ast.html#ast.NodeVisitor). `tokenize.open` supplies encoding-cookie and UTF-8 BOM handling; the scanner limits its iterative walk to statement containers rather than recursively visiting irrelevant expressions. These are standard-library enablers, not new parsing mechanisms. The posture remains a local repair of Test Forge; no renewed whole-skill novelty claim or broad ecosystem survey was needed.

## Assurance calibration

The calibration synthesis adapts these methods; their original regulatory duties, mathematical assumptions, and institutional overhead do not automatically transfer to ordinary software work.

| Primary source | Mechanism reused and operative home | Transfer limit |
|---|---|---|
| FDA, [Computer Software Assurance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software), February 2026 | Risk-based assurance and additional rigor where warranted → calibration's actual-use and consequence analysis | Guidance for medical-device production/quality systems; an analogue for choosing effort, not a regulatory obligation imposed on unrelated projects |
| FDA, [Least Burdensome Provisions](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/least-burdensome-provisions-concept-and-principles), 2019 | Necessary information for the relevant decision, efficient methods and lifecycle timing while preserving requirements → entrypoint objective and total-burden analysis | “Least burdensome” does not authorize lowering a required standard; the portable design choice is this skill's synthesis |
| [NASA-STD-8739.8B](https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/NASA-STD-87398-Revision-B.pdf), §§1.1, 4.4.2.1, 4.5 | Coordinate to avoid duplication; scope and revise assurance rigor according to software risk → recalibration and bounded sibling investigation | NASA's assurance and tailoring authority remain specific to NASA; no universal grade count is imported |
| Dalal and Mallows, [When Should One Stop Testing Software?](https://doi.org/10.1080/01621459.1988.10478676), 1988 ([author-uploaded paper](https://www.researchgate.net/publication/248429057_When_Should_One_Stop_Testing_Software)) | Compare continued testing cost with expected residual losses → calibration's marginal-value question | The mathematical stopping result depends on explicit stochastic and economic assumptions. The skill uses a qualified qualitative judgment when those inputs are unavailable, not a fabricated optimum |
| [JCGM 106:2012](https://www.bipm.org/documents/20126/2071204/JCGM_106_2012_E.pdf), §§8–9 | Decision rules can falsely accept nonconforming results or reject conforming ones → potency's permitted alternatives and oracle error budgets | Measurement uncertainty methods apply under their models; the transferable concern is both directions of decision error, not a universal tolerance |
| Littlewood, Popov, Strigini, and Shryane, [Combining diverse software fault detection techniques](https://openaccess.city.ac.uk/id/eprint/1626/), 2000 | Dependence affects the gain from combining fault-finding methods → source/mechanism/observation independence | This is not empirical calibration of modern agent models. No fixed confidence multiplier follows from changing models or repeating a review |
| Bloomfield and Rushby, [Assessing Confidence with Assurance 2.0](https://openaccess.city.ac.uk/id/eprint/29444/), 2022 | Positive support, counterarguments, and residual doubts → explicit material doubts and bounded closure | Test Forge borrows the questions without requiring their formal assurance-case calculus or claiming logical proof from finite tests |

The earlier investigation also considered Rae et al.'s [Safety clutter](https://doi.org/10.1080/14773996.2018.1491147), 2018. Its duplication/generalization/overspecification framing is an adjacent organizational analogue. The current extension could retrieve a search excerpt but not its full text; it is supporting context, not the sole basis for a rule. The operative retirement rule continues to require demonstrated preservation or loss of function, rather than a low finding count.

Bounded extension date: `20260922`. This revision reused the retained domain investigation and the previously inspected public-skill comparison above, re-inspected the canonical Test Forge plus its local caller references, and rechecked the primary FDA, NASA, JCGM, diverse-detection, and Assurance 2.0 sources. Targeted searches for `"When Should One Stop Testing Software" Dalal Mallows 1988` and `"Safety clutter" "duplication" Rae Provan Weber Dekker` supplied the stopping model and the access limitation above. No new broad marketplace survey or empirical comparison of skills was performed. The decision is to extend the existing skill with CALIBRATE, not claim a new method or create a parallel skill.

The two-axis Pagani objective, protected-quality and owner-authority distinctions, criterion stability, and incidental-friction discipline come from the user's requirements and the local Recompass discussion. Their integration with these research lineages is a design synthesis, not a claim that one cited source establishes the whole procedure. Artifact quality and actual use govern the work; maximizing market adoption is not substituted for them.
