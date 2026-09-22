# CALIBRATE — enough assurance with minimum burden

Use independently to reground an existing plan, or within FORGE, AUDIT, and REFORGE when the assurance design needs judgment. The output is a decision about assurance, not an automatic instruction to build more of it. The sourced methods and their transfer limits are in [lineage.md](lineage.md).

## Ground the decision in actual use

Identify what someone will do because of the result: merge a fix, rely on a recording, delete a source, declare a migration complete, or claim population reliability. Establish the actual path, affected people/data, and supported conditions. Distinguish the artifact being assessed from the report or tool making a claim about it; both can fail in different ways.

Validate the criterion before optimizing its measurement. Does it represent the intended outcome, cover actual use, and preserve named qualities? Separate behavior observed in the artifact, hypotheses about intent, and explicit commitments. A challenge to an assumption is a proposal until it has the requisite authority. Keep criteria comparable across candidates; retain a useful baseline or alternative until the chosen replacement demonstrates preservation of its role. An aggregate score cannot waive a protected obligation.

Define pass, fail, and inconclusive actions before a consequential experiment. Qualify what each means: demonstrated capability on particular inputs, a preserved contract, or an estimate over a population. Passing a convenient proxy does not justify a broader claim. Where priorities involve a real owner tradeoff, present it; resolve technical knowledge gaps through evidence rather than asking the user to guess.

## Locate the consequence without a risk-score ritual

Trace a plausible failure from cause through propagation to observable consequence. Consider these dimensions where they matter:

- **Magnitude and reach:** a visible local error, repeated incorrect output, broad downstream corruption, or irreversible loss.
- **Exposure and coupling:** how often the path is used; whether a shared mechanism can affect many outputs, callers, or future decisions.
- **Detection and recovery:** who would notice, how late, whether rollback restores the meaningful state, and what would already be lost.
- **Uncertainty:** missing observations, changed inputs, unfamiliar mechanisms, correlated authorities, and assumptions the current checks never exercised.
- **Existing protection:** guarantees from simpler design, types, transactions, boundary validation, operational recovery, and independently supported checks.

These are prompts for a causal account, not a compulsory matrix or multiplied ordinal score. A familiar low-stakes product category does not settle the consequences of every operation inside it. Uncertainty alone does not justify maximum machinery either: identify the smallest observation capable of resolving the consequential uncertainty.

For agentic work, include ordinary plausible mistakes: dropped requirements, stale results, changed criteria, copied expectations, wrong selectors, conflated statuses, and edits that bypass assembly. Use deliberately false cases as controlled mistakes. Add adversarial security assumptions only when supported by actual exposure or an explicit threat model; a malicious actor is not needed to justify checking accidental omission.

## Choose the evidence that earns its place

Prefer preventing the error at its natural boundary when a simple mechanism removes the failure opportunity. Then assess the remaining failure paths. Select checks by which consequential uncertainty they resolve, including protection against future regression. A narrow semantic assertion can be stronger than a large integration test; an assembled-path check can expose what all component tests miss.

For a proposed extra layer, answer: what can still go wrong, why would existing controls miss it, what different observation would expose it, and what action would that observation change? Inspect shared assumptions before treating multiple models, reviewers, or implementations as independent. Change the evidence source or observation when their common blind spot is the issue.

Price the whole apparatus: acquisition, execution, maintenance, false acceptance, false rejection, debugging, coordination, context reconstruction, and bugs introduced by the apparatus itself. A cheap permanent guard can earn its place through prevention with no recent findings. A costly replay can also be necessary when it supplies unique consequential evidence. Neither lowest runtime nor maximum rigor alone optimizes the outcome.

Borrow the economic question from sequential testing: is the next observation's plausible decision or protection value worth its total burden? Quantify only where defensible probabilities, losses, and sampling assumptions exist. Otherwise use a transparent qualitative comparison and identify what would change it. Do not turn unknowns into invented expected-loss numbers or equate every harm through one scalar.

Remove incidental friction while preserving guarantees. When a stronger design materially improves assurance, keep it visible and simplify its use. When an irreducible tradeoff remains, make it owner-visible; never silently lower a commitment to make the apparatus cheaper. Preserve applicable closure requirements, including mandated falsifiers. Satisfy each requirement with a relevant, bounded check rather than an unrelated campaign; a conflicting requirement needs explicit resolution, not a hidden waiver.

## Bound depth and expansion

Use source-grounded requirements and expected values to check construction. Challenge the parts of the evidence machinery whose own failure could change the decision, especially admission, expected values, comparisons, and status interpretation. Then stop the recursive expansion at its explicit proof limit unless a named material doubt calls for a further distinct check. A second checker built from the same untested premise is not an escape from that limit.

Predeclare an informative first batch, its limits, and the finding that would justify expansion. A discovered shared fixture fault can justify checking sibling claims; a local unrelated typo does not justify an entire new audit. Fix the cause and test the implicated family. Once relevant checks pass, repeat or broaden only for a changed result, unresolved doubt, or required cadence.

When estimating rates, use a sampling and stopping method that supports the intended statistical claim. Repeatedly inspecting results and stopping on a favorable sample cannot silently inherit a fixed-sample confidence statement. A capability example or a set of hand-picked mutants supplies no general reliability percentage.

The practical stopping point is conditional: the scoped obligations have the required evidence, material counterarguments are addressed or remain explicitly limiting, and another proposed activity has no justified distinct role. This is a revisable engineering judgment, not proof of zero defects or a universal optimum. Keep the assumption or event that would reopen it visible.

## Deliver a bounded disposition

Use a short paragraph for a simple recalibration. For consequential apparatus work, use the shared decision/claim record in SKILL.md; do not create a parallel mandatory template. State the next supported move:

- **Keep / no intervention:** existing evidence supports the scoped decision and the proposed change adds no useful role.
- **Add or repair:** name the missed failure, smallest relevant check, and required authority.
- **Simplify or replace:** name the burden removed and the evidence preserved.
- **Investigate:** name the unresolved question, bounded informative observation, and expansion condition.
- **Stop with a limit:** state whether the decision is supported, failed, or inconclusive, and what evidence remains unavailable.

Retire a control only after showing redundancy, replacement, or loss of its function. Use the bounded preservation argument in [audit.md](audit.md); retain unique prevention, compatibility, diagnostic, and regression roles. A period without findings is not that argument. Retain temporary apparatus only for a named continuing function; keep necessary results and reproduction identities in the project's existing evidence home, then remove proven disposable scaffolding within authority.

Recalibrate when use, inputs, claims, code, consequences, or control behavior materially change. Reuse evidence where its identity and assumptions remain compatible. Avoid periodic ceremonies or repeated permission questions for already authorized work.
