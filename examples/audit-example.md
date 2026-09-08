# Worked example — execution-first apparatus audit

## Input

Historical case-study measurements below describe distinct captured runs, not a fresh verification or one additive collection census. Apply the current decision-before-cost gate before reproducing expensive work.

A local embedding server had 587 collected pytest cases, a routine suite, scheduled model acquisition, platform lifecycle jobs, and a large slow HTTP module. The prompt was to determine whether the suite was trustworthy and how much effort was pointless.

## Execution census

The first pass bound the revision, read `pyproject.toml` and CI before interpreting test results, and recorded:

- 531 passed, 2 skipped, and 56 deselected under the default `not slow` selector;
- 24.48 seconds warm and 38.66 seconds colder;
- 31 slow HTTP cases, with no CI command naming their module;
- a scheduled lifecycle command that acquired all model snapshots and then invoked a slow-marked file without `-m slow`.

Collection under the exact scheduled command showed that all four lifecycle tests were deselected. This was the highest-severity finding: the apparatus paid the setup cost and emitted green without executing the evidence its job name promised.

## Proof-obligation sample

| Claim | Failure that must be observable | Authority and seam | Existing problem |
|---|---|---|---|
| HTTP validation rejects over-limit input | inclusive boundary or prefix miscount admits/rejects the wrong request | real application; real tokenizer only where tokenization decides admission | full real model loaded for an HTTP decision made before inference |
| Python client interoperates with the server | serialization or socket behavior differs from in-process calls | real TCP listener with deterministic server core | real-model cost attached to a transport claim |
| Default model returns useful normalized embeddings | backend or task-prefix behavior changes numeric output | locked real model and semantic/numeric oracle | separate forwards repeated compatible setup and inputs |
| Installed wheel discovers adapters outside the checkout | entry point absent or source tree leaks into import | installed wheel contents plus fresh interpreter | new venv and package-manager startup repeated per test |
| launchd lifecycle works | install/wake/embed/idle/remove path fails on macOS | real OS lifecycle with acquired artifacts | intended tests never selected |

## Assertion audit

The smell scanner seeded five candidates. Manual inspection confirmed three vacuity/conditional issues and rejected two false positives. The slow server suite also contained stale imports and repeated validation, CORS, schema, readiness, and error claims already established at a narrower authoritative seam.

The audit did not call every real-model test redundant. It retained model numerics, a real tokenizer boundary, and lifecycle evidence because those components or boundaries were the subject of the claims.

## Cost attribution

Durations showed distinct causes rather than one generic “slow suite”:

- repeated model loads and neural forwards;
- fixed sleeps whose planted blockers survived into teardown;
- repeated virtual-environment and pip startup;
- duplicated fixture and local-server implementations;
- broad protocol matrices rerun through an irrelevant real model.

Each optimization recommendation named the evidence preserved. The 100-request concurrent counter regression remained because it alone exercised a lost-update failure surface.

## Output

The audit produced:

1. the exact execution baseline and hidden-selector defect;
2. a claim-to-evidence map with seam, cadence, cost, and proof limits;
3. assertion-level false-confidence findings;
4. dominance candidates for the duplicated slow HTTP matrix;
5. a dependency-ordered REFORGE topology.

The decisive move was auditing whether evidence ran before judging what green meant. A taxonomy-only audit would have found weak assertions but missed the costliest false assurance.
