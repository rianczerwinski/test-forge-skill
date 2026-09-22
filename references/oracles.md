# Oracle authority and numerical evidence

Choose the expected-value authority for the particular claim. Independence limits correlated mistakes; it does not guarantee that the reference, specification, or physical model is correct.

First establish that the criterion represents the intended use and explicit commitments. A perfectly enforced proxy can be the wrong target. Distinguish a proposed reinterpretation from owner authority and report criterion changes separately from improvements measured under them.

## Available authorities

- **Specified or analytic:** an explicit contract, hand calculation, or known result. Check that the asserted behavior follows from the cited authority.
- **Differential:** compare independently implemented mechanisms on identical inputs. Agreement supports conformance under shared assumptions; common dependencies or shared defects can weaken independence.
- **Metamorphic:** assert a justified relation between related inputs/outputs. State its preconditions; a relation may hold while absolute values remain wrong.
- **Captured reference:** preserve trusted reference outputs with input identity, version/model hash, generator, and capture conditions. This retains authority for those cases without rerunning the reference.
- **Regression capture:** preserve prior behavior without implying independent correctness. Document whether it was independently validated at capture time.

Compare authority, relevance, input coverage, and freshness; no technique is universally stronger than snapshots. Read [potency.md](potency.md) for sensitivity and valid-alternative checks.

Assess dependence through shared sources, assumptions, mechanisms, and observations. Several agents repeating a source or inheriting the same implementation summary do not supply a confidence multiplier. A different model can contribute a useful interpretation; establish what evidence or failure search is actually different before claiming independence.

## Model ports and reference cost

Separate reference conformance from other promises such as error handling, numerical stability, performance, and integration behavior. Matching a reference is one scoped obligation; it does not discharge all product correctness.

Choose live test-only reference execution, provenance-locked captures, or vetted upstream vectors according to the claim, drift risk, environment, and cost. A cheap captured-reference routine suite plus a separately reachable live comparison is useful when reference drift matters, but is not compulsory. Keep a reference out of production dependencies when runtime independence is part of the product's purpose.

Bind expected data to its actual source and compatible inputs. Regeneration from the port cannot silently retain an independent-reference label. For captured fixtures, preserve the trusted generator and enough input identity to reproduce the case.

## Planted truth and shared mechanisms

Generate inputs from an independently justified forward model when testing inverse/estimation behavior. Inspect whether generator and estimator could reproduce the same sign, coordinate, calibration, or modeling mistake.

Keep ground truth flowing from generator to assertion and make the relevant independence visible in the repository. Shared file utilities or unrelated infrastructure need not invalidate it; sharing the mechanism whose correctness is disputed can. Choose one or multiple generators based on the failure families represented, rather than imposing a universal directory or generator count.

Pair synthetic evidence with real observations or additional authorities where model mismatch could defeat the claim. When direct expected outputs are unavailable, use justified relations and state the remaining oracle gap.

## Tolerances and valid alternatives

State the measured quantity and units, consequential error limit, known numerical/measurement variability, and supported conditions. Choose tolerances from that error budget, including absolute versus relative behavior near zero. Quantify uncertainty with an appropriate domain method when the claim is statistical.

Challenge the threshold with relevant wrong outputs and permitted variation. Tightening to an observed noise floor can reject valid implementations; a wide absolute tolerance can be meaningful on a different scale. Avoid deriving a universal threshold from a fixed multiple of the current quantity.

Compare unordered outputs under the permitted equivalence, such as speaker-label permutation or valid result order. Verify content/grouping as well as count. Name empirical quality claims honestly rather than presenting a small successful sample as a population guarantee.

## Negative controls

Observe a relevant rejection before treating a new consequential oracle as demonstrated sensitive. A pre-fix failing example, controlled bad output, or isolated mechanism mutation can supply it. If a disabled mechanism still passes, determine whether the mutation activated, changed behavior, propagated, and was observed, or whether an allowed fallback preserved the claim.

Use the shared falsification protocol in [potency.md](potency.md). A killed mutant cannot make a circular expectation independent, and a surviving equivalent implementation is not automatically a test defect.
