# Potency — make a test discriminate

Use this shared procedure in FORGE for new or materially changed consequential assertions, in AUDIT for evidence assessment, and in REFORGE for retained or rebuilt evidence. A routine execution of unchanged tests does not require repeating the procedure.

## The causal check

Name a plausible violation of the sourced claim and trace:

1. **Valid setup:** the fixture, input, state/history, and environment activate the intended situation. Confirm that setup, mocks, or guards did not bypass it.
2. **Reach and activate:** execution reaches the faulty behavior and creates a relevant incorrect state. Coverage alone establishes neither activation nor incorrectness.
3. **Propagate:** that state affects a result at the chosen seam; a later overwrite, retry, cache, fallback, or cancellation may mask it.
4. **Observe and reject:** the asserted quantity exposes the error and the acceptance rule rejects it for the intended reason.
5. **Accept permitted behavior:** correct alternatives remain accepted—label/order permutations, equivalent algorithms, supported environments, and allowed numerical variability.

This uses RIPR's fault-detection chain and adds explicit setup and valid-alternative scrutiny; see [lineage.md](lineage.md). Also inspect expected-value authority: a perfectly sensitive test can enforce the wrong requirement.

For a bounded change, a short explanation or relevant pre-fix failure may suffice. For consequential assurance or apparatus redesign, retain the claim, case, authority, observed outcome, and scope limit. Judge potency for the named fault family; one live assertion says little about omitted families.

## Select useful falsifiers

Start with a real pre-fix failure when it matches the current claim and conditions. Otherwise choose a small false behavior that could defeat the requirement: inclusive/exclusive boundary change, dropped side effect, wrong collaborator, incorrect grouping, missing selector, or corrupted identity. Mutate a fixture or result if that isolates the oracle's discrimination; mutate production/configuration if the claim concerns end-to-end detection. State which was tested.

Automated mutation tools are useful when supported operators and bounded runtime add signal. Triage survivors rather than pursuing a universal score. A broad campaign is warranted by the task's stakes or demonstrated missing detections, not by the mere existence of a test file.

## Isolated falsification protocol

1. Use an isolated copy or repository-approved isolated environment; preserve original bytes and existing user changes. Bind the source, inputs, configuration, and selector relevant to the claim. Avoid live production and external mutations without specific authority.
2. Run the unchanged baseline with nonempty intended selection. Resolve or separately identify existing failures before attributing a new one.
3. Apply one named perturbation and verify the exact intended change. Keep time/resource bounds appropriate to the run.
4. Execute the same evidence path. Inspect which assertion/check rejected it and why. Credit a syntax, import, collection, setup, or timeout failure only when it demonstrates the named violated claim; for example, a missing packaged module can expose a promised importability failure. An unrelated failure that prevents the target behavior from being assessed is inconclusive, whatever its category.
5. Classify the result, restore exact original bytes/configuration, check the owned diff, and rerun the baseline. Preserve the concise evidence needed to understand the result; retire an isolated disposable copy after that evidence is retained.

## Interpret results

| Observation | Interpretation and next action |
|---|---|
| Relevant rejection at the intended assertion/check | Sensitivity demonstrated for this case; inspect authority and coverage limits separately |
| Mutant was not applied or the scenario never reached it | Invalid probe; repair setup or choose an applicable perturbation |
| Mutation changes internal state but is masked before observation | Investigate propagation or the seam; valid recovery may preserve the claim |
| Wrong observable result passes | Oracle gap; strengthen the relevant observation or acceptance rule |
| Equivalent behavior or valid fallback passes | Potentially correct acceptance; confirm equivalence within the claimed scope |
| Correct supported behavior fails | Overspecification, invalid tolerance, or setup defect; repair the test |
| A failure prevents assessment of the named claim, or the run is unavailable | Inconclusive; preserve diagnostics and state the outstanding evidence |

Report the first failed attempt separately from reruns. For nondeterministic failures retain inputs, seed, order/history, environment, and relevant timing; a seed is not a complete replay identity.

## Enforcement and limits

Enforce what the apparatus can decide: selected-test counts, explicit error statuses, required selector presence, configured cost bounds, and reproducible behavioral regression checks. Use semantic reasoning for obligation relevance, plausible faults, oracle authority, and permitted equivalence. A validator checking that these fields are populated cannot establish those judgments.

Separate test sensitivity from system completeness and readiness. Mutants selected alongside assertions are known examples; reserve defect-recall calibration for an independently chosen defect population with a stated sampling method.
