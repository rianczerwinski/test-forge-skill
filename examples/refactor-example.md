# Worked example — a first-principles refactor chart

The design output for the same `relata` suite: not a patch-list of the audit findings, but a ground-up rebuild. Shows how the taxonomy drives the whole refactor.

## The root reframe

The wrong question was "how much coverage" (1.08:1 — looks great, means nothing). The right one: **for each thing under test, does a test exist that could actually fail if it were wrong?** Every audit finding was one disease — *category collapse* — a test claiming a stronger kind than its assertion delivered. So the refactor is a taxonomy refactor, not a rewrite.

## The spine: assign required kinds per module

| relata module | Character | Required floor |
|---|---|---|
| `inference/`, `frontend/`, `enhancement/`, `calibration/` | numeric core | Oracle + Property + negative control |
| `streaming/`, EKF trackers | stateful | Property + Contract; Oracle where truth is knowable |
| `protocol/`, `storage/`, audio IO | IO | Contract + Smoke |
| CLI, session integration | glue/integration | Contract + Smoke |

A numeric module whose only coverage is Smoke has *no correctness coverage* — that framing turned the audit's scattered findings into a single actionable gate.

## Solving the two oracle problems (the real work)

**Problem 1 — the numpy ports.** The library's whole thesis is "numpy replicates torch with no torch at runtime." The only oracle for that is torch. The current goldens faked it (captured numpy's own output → circular). Resolution offered as a fork: (a) torch as a *test-only* dep, regenerate expecteds from the real model every CI run (differential testing done right); (b) capture-once from the reference, provenance-locked; (c) vendored reference pairs. Lean: **(b) every run + (a) gated behind `RUN_ORACLE=1`** — honest goldens always, a true reference oracle on demand, no heavy dep in the default path (mirroring the suite's existing `RELATA_REAL_ASR` pattern).

**Problem 2 — the DSP scenes.** Estimators tested on synthetic scenes where the answer is planted. Sound only if the scene is generated *independently* of the estimator — the near-field test failed because it wasn't. Fix is structural: **one independent scene generator** in `tests/scenes/` (analytic delay-and-superpose / image-source room model), imported by no estimator; ground truth flows one way.

## Enforcing sensitivity

The `test_joint_ekf_tolerance` test already had the antidote — a negative control proving DOA error *explodes* without re-estimation. Generalize to a law: **an assertion never seen fail is not known to be able to fail.** Every accuracy claim gets a paired negative control; mutation testing (mutmut) backstops the numeric core only.

## Target structure — mirror source, not episodes

```
tests/
  scenes/       ← the one independent generator
  oracle/       ← reference goldens + provenance manifest
  unit/<subsystem>/  ← mirrors src/relata/<subsystem>/
  property/  integration/  contract/  regression/  smoke/
  conftest.py   ← one stub-provider, one fake-model, one factory
```

The episode files (`wave_*`, `*_upgrades`, `r1_restructuring`, `novel_approaches` citing "Plane 5 §5.3") dissolve: real tests migrate into the mirrored tree under the right marker, scaffolding is deleted, workstream IDs leave the docstrings.

## Phased migration (can't rewrite 38k LOC atomically)

- **Phase 0** — five kind-markers + required-kinds table; gate only *new* tests. Touches nothing.
- **Phase 1** — triage sweep (= the audit, executed): delete dead/tautological/can't-fail, relabel goldens.
- **Phase 2** — fill oracle gaps (stand up the two generators; every numeric module gets an oracle + negative control). The real project; blocks on the oracle forks.
- **Phase 3** — consolidate: mirror the tree, hoist fixtures, dissolve episode files.
- **Phase 4** — flip the gate to all tests; mutation-test the numeric core.

Phases 1 and 3 start immediately from the audit. Phase 2 blocks on decisions — surfaced as forks, not picked silently.

## The forks left to the user (not decided silently)

Oracle strategy (1a/1b/1c), delete-vs-quarantine, CI gate hard-or-advisory, mutation-testing adopt-or-manual, scope (full vs numeric-core-only), and whether the chart becomes a persisted ADR. Each reflects the user's values, not a technical necessity — so each was presented, not chosen.
