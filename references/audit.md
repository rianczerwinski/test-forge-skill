# AUDIT — determine whether a test apparatus is trustworthy

Audit the apparatus in the order that evidence becomes usable: execution, obligations, individual assertions, duplication, and closure. A green result has no meaning until the audit establishes what was selected and which claim the selected evidence can support.

## 1. Freeze the baseline

Bind the source revision and preserve existing user changes. Read the test-runner configuration, dependency groups, project test documentation, and CI/release workflows before running commands.

Record:

- collected, selected, passed, failed, skipped, expected-failure, deselected, and warning counts;
- the exact routine command and every documented or CI evidence-plane command;
- environmental and optional-dependency gates;
- cold and warm runtime when model, compiler, container, or artifact initialization is material;
- slowest setup, call, and teardown phases when the runner exposes them;
- CPU, memory, disk, network, or external-service costs when they can constrain cadence.

Selection is an object of audit. Run collection under the exact marker expression and environment used by CI when feasible. Confirm that a command naming a file actually admits its intended tests; runner-level defaults can still deselect them.

Do not install missing optional dependencies merely to make the census look complete unless the task authorizes environment changes. Record the unavailable evidence and where it is expected to run.

## 2. Derive the proof-obligation population

Read externally meaningful claims from specifications, public APIs, user workflows, architecture, state transitions, incident history, fixed defects, compatibility promises, deployment behavior, and release documentation. Source modules help locate evidence; they are not the population denominator.

For each obligation, record:

```text
Claim:
Failure and propagation:
Truth kind and independent authority:
Required architectural seam:
Current evidence and selector:
Cadence and measured cost:
Falsifier status:
Proof limit:
```

Name propagation far enough to make seam choice possible. “Client request breaks” may decompose into client serialization, TCP transport, server validation, model inference, and response decoding; each can require different evidence.

When the requested scope is a systematic whole-codebase or release-readiness assurance audit, consume the risk topology from Audit Planes rather than inventing a second exhaustive census. Test Forge still evaluates and restructures the resulting test evidence.

## 3. Inspect assertion honesty

Classify what each consequential test actually establishes using [taxonomy.md](taxonomy.md), then compare it with the claim attached to it. Run `scripts/smell-scan.py` on Python suites to seed candidates, and manually inspect all material candidates plus high-consequence tests it cannot understand.

Prioritize false confidence over waste:

1. a test that stays green through the defect it names;
2. an external claim whose only evidence is skipped, deselected, stale, or unavailable;
3. a test whose authority is circular or whose seam bypasses the failure;
4. unique but flaky or operationally unreachable evidence;
5. redundant or accidentally expensive evidence.

Every finding should include location, claimed versus delivered truth, named failure surface, consequence, evidence, and one disposition: fix, strengthen, relocate, merge, delete, or record a proof gap.

## 4. Analyze seams and doubles

For each claim, ask whether the current test crosses too little or too much architecture.

- **Too narrow:** the test bypasses the boundary where the named defect occurs, such as using an in-process client to claim socket compatibility.
- **Too broad:** the test loads a real model, database, browser, or external service for a decision already made by validation or routing code.
- **Well placed:** every real boundary is necessary to observe the failure, and every substituted component is outside the subject of the claim.

Do not rank tests on a unit→integration→end-to-end realism gradient. A narrower Contract test can be authoritative for one claim while a fresh-process Smoke test is necessary for another.

## 5. Establish evidential dominance

Call a test removable as redundant only when another reachable evidence path:

- supports the same claim with equal or stronger authority;
- preserves every failure surface the candidate can observe;
- runs at an equal or more useful cadence;
- retains any negative-control, compatibility, platform, or diagnostic role;
- and does not merely share line or branch coverage.

Broader execution is not automatically stronger. Coverage-equivalent reduction is not proof-preserving; empirical test-suite-reduction research has found substantial losses in fault detection. When uncertainty remains, keep the test or validate the proposed deletion with representative mutants before removing it.

## 6. Attribute cost

Separate essential from accidental cost:

- setup repeated across tests that could share an immutable fixture;
- inference or compilation repeated for compatible inputs that could batch;
- arbitrary sleeps used as synchronization;
- teardown waiting for planted blockers or leaked executors;
- racy free-port discovery instead of passing an already-bound socket;
- process, environment, or package-manager setup irrelevant to the claim;
- duplicated matrices repeated at broader seams.

Cost findings state both time saved and evidence preserved. “Delete because slow” is not a valid recommendation.

## 7. Audit reachability and truth states

Inspect configuration, workflow YAML, scripts, dependency installation, environment variables, and generated-artifact steps as part of the apparatus.

- Distinguish pass, expected failure, skip, deselection, empty collection, warning, setup failure, and unavailable environment.
- Verify scheduled/manual commands contain the selectors required to override routine exclusions.
- Verify generated fixtures or manifests are refreshed or revision-bound before their consumers run.
- Promote actionable deprecations or compatibility warnings into dependency/configuration work; do not normalize them through blanket suppression.
- Ensure documentation names exact commands and the claims each command discharges.

## 8. Deliver the audit

Return:

1. **Baseline:** revision, commands, selection states, timings, environments, and proof limits.
2. **Significance-first findings:** false confidence and missing evidence before waste.
3. **Claim-to-evidence map:** obligations, authority, seams, selectors, cadence, falsifiers, and gaps.
4. **Dominance candidates:** exact delete/merge/relocate opportunities with the evidence-preservation argument.
5. **Reforge topology:** dependency-ordered changes, without implementing them unless the user authorized refactoring.

Report a redundancy percentage only with an explicit denominator and equivalence method. Treat a clean smell scan as supporting evidence while the claim map, reachability, oracle provenance, and semantic review determine trustworthiness.
