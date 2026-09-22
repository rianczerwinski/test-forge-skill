# REFORGE — streamline a test apparatus

Preserve scoped claims while improving test authority, potency, placement, runtime, and maintenance cost. Keep production behavior fixed unless the user also authorizes production fixes.

## Establish what must survive

Use [audit.md](audit.md) for an affordable baseline and obligation population. Apply the decision-before-cost gate before any expensive baseline. A broken test can expose either a product defect or an apparatus defect; determine which before editing.

Apply [calibration.md](calibration.md) before selecting the replacement. Optimize assurance and the cost of operating it together, including false alarms and coordination. First consider whether simplifying the product or enforcing an invariant at its owner eliminates a failure opportunity; propose production changes separately when outside authority. A redesign need not add machinery, and a healthy part need not change.

Map claims to authority, material failure paths, seams, selectors, cadence, and proof limits. Group common setup after identifying these obligations. Source modules provide navigation, not an automatic completeness denominator.

Keep comparison criteria stable and name protected qualities. Preserve the baseline or candidate with a unique useful role until the replacement demonstrates that role. Report justified criterion changes separately; do not bury lost guarantees inside a faster runtime or higher aggregate score.

## Choose boundaries by the failure

Select from a palette: pure computation; in-process subsystem/application; thread/process behavior; socket/IPC; built or installed artifact; real dependency compatibility; OS lifecycle; user journey. These boundaries are not a total order. Retain the boundaries that introduce distinct failure modes without replaying every inner edge case at each outer boundary.

Use real HTTP policy with a deterministic model for validation and routing; real sockets for transport; real tokenization where token counts decide admission; real inference/reference data for numerical or semantic claims. Check fake conformance when the conclusion depends on the represented dependency's behavior.

## Shape cost without changing the claim

- Share expensive immutable acquisition and setup at the narrowest fixture lifetime preserving isolation. Reset mutable state explicitly.
- Batch compatible inputs when batch behavior is not itself an uncontrolled variable; keep failures diagnostic.
- Replace synchronization sleeps with events/barriers or observable state; use fake clocks only when they preserve the time behavior under test. Release planted blockers in teardown.
- Bind sockets before handing them to servers where supported; avoid discovering a free port and binding it later.
- Use a fresh interpreter for import-isolation claims and the real package manager for installation claims. Include only the environment machinery required by the boundary.
- Resolve actionable migration warnings at their owner; avoid global suppression that hides distinct new warnings.

Measure comparable commands after each coherent cluster. Include setup and teardown; retain original failures separately from retries.

## Consolidate with a bounded preservation argument

Apply the dominance criteria in [audit.md](audit.md) before deletion. Parameterize or share setup when authority and seams match. Retain unique platform, history, boundary, and negative-control roles even when they share coverage with other tests.

Assign surviving tests to durable behavioral owners. Source mirroring, protocol, lifecycle, and cross-cutting property suites are alternatives selected for discoverability. Move evidence out of episode-named files only when ownership improves, then remove an emptied shell after verifying it has no remaining role. Use Repo Refiner for material tree/navigation reconciliation instead of recreating its procedure.

## Repair reachability

For each applicable evidence plane, document the exact command, environment/dependencies, expected admission, claims, cadence, and approximate cost. Use the project's existing runner and CI mechanisms to enforce critical admission and bounds.

Selection-check nonroutine paths and run affected affordable evidence within authority. A selection check for an unavailable platform is useful but cannot discharge runtime behavior there. Add targeted regressions where a workflow edit could silently acquire artifacts and deselect the promised tests.

## Attack and finish

Apply [potency.md](potency.md) to new or changed consequential evidence and to representative retained claims affected by fixture/configuration changes. Choose false behaviors from obligations: changed inclusive boundaries, omitted side effects, wrong routing, bypassed compatibility boundaries, corrupted identities, or removed selectors. Use isolated copies and record expected rejection versus unrelated failure.

Check permitted transformations too: reordered labels, equivalent implementations, supported platforms, and allowed variability. A rebuilt suite that kills mutants but rejects valid behavior is unfinished.

Retain the choice/evidence/rejected-alternative/validation trace requested by the user or needed for maintenance, including before/after commands, bounded deletion arguments, falsification, and proof limits. Run affected checks, inspect the diff for weakened assertions/selectors, and remediate failures before closing.

Report completed implementation separately from system readiness. A refactor may preserve an existing explicitly unavailable evidence plane; it cannot report that plane as passed or silently retire its obligation.

Recalibrate after a finding changes the failure population; investigate implicated siblings without expanding automatically to the whole system. Honor governing closure checks, then stop when the scoped evidence is supported and no named material doubt warrants another distinct check. Remove proven redundant scaffolding while retaining evidence needed to understand, reproduce, or maintain the result.
