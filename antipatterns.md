# Anti-patterns

Use these contrasts to inspect claims and failure paths, not to classify tests from spelling alone.

## Contents

Authority and assertion potency; experiment sizing; seams and execution; reduction and closure; assurance calibration.

### Circular golden

❌ Wrong: capture the current port's output, then label comparison with that capture an independent-reference accuracy test.

✅ Right: retain it as an honestly labeled regression, or compare against provenance-locked outputs from an independently justified authority.

Why it flips: a stable output can still be wrong; the expected value's origin determines what agreement supports.

### Guarded-away failure

❌ Wrong: `if model.converged: assert model.error < budget` in a test claiming convergence.

✅ Right: assert convergence before checking error. Express a genuinely unavailable environmental prerequisite as an explicit skip with its proof limit.

Why it flips: failure of the named behavior must reach a rejection, while environmental absence must remain visible.

### Correlated calculation

❌ Wrong: derive both estimator input and expected answer from the estimator's disputed geometry/sign convention, then claim physical accuracy.

✅ Right: use independently justified planted geometry and inspect shared mechanisms capable of reproducing the same error.

Why it flips: tight agreement can demonstrate shared assumptions rather than correctness. Repeated calls such as `f(x) == f(x)` are not automatically tautologies; stateful or randomized calls can differ.

### Range posing as accuracy

❌ Wrong: claim source localization accuracy from `0 <= azimuth < 360` alone.

✅ Right: compare with planted truth under a justified angular error budget, including periodic angle equivalence where applicable; keep the range assertion as a separate validity contract.

Why it flips: the range can detect invalid outputs but cannot distinguish correct localization from an arbitrary valid angle.

### Decorative or over-tight tolerance

❌ Wrong: widen a threshold until green, or tighten it to one machine's observed noise floor.

✅ Right: derive the acceptance range from units, consequential error, supported conditions, and legitimate numerical variability; challenge it with bad outputs and valid alternatives.

Why it flips: both false acceptance and false rejection matter. Scale alone cannot supply a universal tolerance.

### Mock-shadow

❌ Wrong: configure a separator mock to return three outputs, exercise the wrapper, and claim the separation algorithm works because three outputs were returned.

✅ Right: use that fixture for wrapper routing/pass-through behavior. Test separation quality using the relevant real mechanism and independently justified references, respecting output permutation.

Why it flips: the wrapper did execute; the substituted algorithm did not. A configured return value is legitimate evidence for some contracts, not for the substituted component's quality.

### Static-grep-as-behavior

❌ Wrong: assert that source text lacks `executor.*run_dsp` to establish the actual execution thread.

✅ Right: observe the thread executing DSP; retain source-pattern checks only for an explicitly structural policy.

Why it flips: behavior-preserving edits can change spelling, and behavior-changing edits can preserve it.

### Speaker count posing as discrimination

❌ Wrong: `len(set(ids)) == 2` is the entire evidence that two speakers were correctly distinguished.

✅ Right: compare segment grouping against independently labeled segments while accepting arbitrary speaker-label permutation; see [examples/potency-example.md](examples/potency-example.md).

Why it flips: alternating arbitrary labels can satisfy the count while grouping speakers incorrectly. Liveness-only evidence remains useful when labeled as smoke.

### Capability gate becomes a survey

❌ Wrong: launch every microphone/session combination to answer whether the basic path works, before inspecting a result or measuring throughput.

✅ Right: name the capability decision, choose an informative bounded first batch, and state pass/fail/inconclusive actions and expansion conditions. Reserve a justified population design for reliability claims.

Why it flips: stronger per-test assertions cannot rescue an experiment that spends on a different question. Neither a fixed two-case gate nor a full matrix is universal.

### Realism gradient

❌ Wrong: replay the full HTTP validation matrix through a downloaded model solely because it feels more integrated.

✅ Right: exercise the real application policy with a deterministic model, retaining real-model evidence for the distinct model/server behavior.

Why it flips: irrelevant inner execution adds cost without adding authority to the outer claim.

### Selector illusion

❌ Wrong: assume naming a slow test file overrides the runner's default `not slow` selector.

✅ Right: inspect and selection-check the exact nonroutine command, including the explicit selector needed by that runner, before expensive acquisition.

Why it flips: a job can acquire everything and still admit none of its promised tests.

### Marker-count assurance

❌ Wrong: credit a module because nearby tests have Oracle and Property markers.

✅ Right: map sourced claims to inspected assertions and actual execution; use markers for selection or navigation.

Why it flips: metadata neither validates authority nor proves a relevant assertion executed.

### Planted-sleep synchronization

❌ Wrong: make a worker sleep long enough to trigger a timeout, then pay the remaining sleep during teardown.

✅ Right: hold it with an event, observe the timeout, and release the event in a finally block. Test real elapsed time only when that is the subject.

Why it flips: observable synchronization preserves the failure condition while avoiding accidental teardown latency.

### Isolation theatre

❌ Wrong: rebuild an environment for each test whose claim is only pure-wheel entry-point discovery outside the checkout.

✅ Right: use controlled wheel contents with a fresh isolated interpreter for that claim; use actual installation machinery for the separate package-manager claim.

Why it flips: choose isolation that preserves the named boundary, not every available layer of setup.

### Episode-named ownership

❌ Wrong: leave live evidence split among wave, migration, and redteam-episode files after the episode ends.

✅ Right: move it to the enduring subsystem, contract, or lifecycle owner when that improves navigation; remove the emptied shell after checking its remaining roles.

Why it flips: durable behavioral ownership makes future evidence discoverable without requiring a universal source-mirroring layout.

### Reduction by count or coverage

❌ Wrong: delete tests because they cover the same lines or because representative mutants were all killed.

✅ Right: document surviving authority, fault families, inputs/histories, environment, cadence, and diagnostic roles. Preserve uncertain unique evidence until its replacement is demonstrated; a written follow-up alone does not authorize removal. Any owner-authorized evidence gap remains explicit.

Why it flips: a scoped preservation argument is stronger than structural overlap; finite probes do not establish universal equivalence.

### Wrong-reason mutation kill

❌ Wrong: break an import, watch the suite fail collection, and credit detection of a wrong numerical result.

✅ Right: baseline nonempty selection, apply the relevant mutation in an isolated copy, observe the intended assertion reject it, restore exact bytes, and rerun.

Why it flips: relevance to the claim decides whether the kill is useful. An import failure is inconclusive for numerical accuracy but can be the intended rejection for a packaged-module importability claim.

### Survivor automatically means inert

❌ Wrong: disable a component, see green, and immediately declare the test powerless.

✅ Right: distinguish invalid perturbation, missed activation, masking, valid fallback, equivalent behavior, and an actual oracle gap.

Why it flips: the claim may still hold; potency concerns incorrect behavior rather than implementation difference itself.

### Retry erases failure

❌ Wrong: report only a successful retry or silently quarantine the failing evidence.

✅ Right: retain the first outcome and replay context, identify the instability's owner, and give quarantine an exit condition and explicit proof gap.

Why it flips: later success does not explain the original failure or discharge its obligation.

### Failed inspection becomes clean

❌ Wrong: warn about a parse failure, count the file as inspected, and return a successful no-candidates summary.

✅ Right: report discovered and parsed populations separately, retain partial findings, and return the documented incomplete-inspection status.

Why it flips: absence of findings in unreadable material is absence of evidence.

### Captured gap becomes closure

❌ Wrong: mark system readiness established because each obligation has either a passing test or a written gap.

✅ Right: complete the bounded diagnosis while naming unmet readiness obligations separately; close readiness only when its required evidence is discharged.

Why it flips: preservation of uncertainty and resolution of uncertainty are different outcomes.

### Product label substitutes for consequence

❌ Wrong: “It's an audio library, so persistence checks are excessive”; or “agents wrote it, so every edit requires maximum assurance.”

✅ Right: trace the actual failure, exposure, visibility, recovery, and existing protection. Scale effort to the operation: a display typo and deleting the only recording have different consequences.

Why it flips: category and authorship are prompts for inspection, not evidence of a particular risk level.

### Assurance earns another assurance layer

❌ Wrong: add a checker of each checker indefinitely, or mandate the same number of independent reviews for every claim.

✅ Right: name the material doubt and the different evidence that could change the decision. Challenge consequential weaknesses, satisfy governing closure requirements, and stop with explicit limits when another layer has no justified distinct role.

Why it flips: depth follows a failure of the evidence path; counting layers cannot establish independence or completeness.

### Moving the goal manufactures progress

❌ Wrong: loosen the quality threshold after seeing a failure, report improvement, and hide a protected-case regression in the average.

✅ Right: justify any criterion change against actual use and owner commitments, evaluate comparable candidates, and report the protected failure separately.

Why it flips: a change in the measure is a different claim from a change in the measured object.

### Quiet protection looks disposable

❌ Wrong: retire a cheap recovery regression because it has found no new defects this quarter.

✅ Right: retain its prevention and compatibility value unless a reachable replacement preserves its role or the requirement is legitimately retired.

Why it flips: a useful control's value includes failures prevented and guarantees preserved, not only fresh findings.

### Different model becomes independent evidence

❌ Wrong: give three agents the same completion summary and assign their agreement triple evidentiary weight.

✅ Right: identify shared assumptions and inspect original requirements, results, and the actual operating path where those resolve the doubt. Credit different scrutiny only for what it actually examined.

Why it flips: model identity and assigned posture do not establish independent sources, observations, or error rates.

### Calibration becomes compulsory ceremony

❌ Wrong: produce a risk matrix and new evidence ledger before every run of an unchanged local test.

✅ Right: use the known command and gates, report its actual result, and expand calibration only when the decision, consequence, uncertainty, or apparatus calls for it.

Why it flips: the methodology's own burden belongs in the optimization; the form is not the assurance.
