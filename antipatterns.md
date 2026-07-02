# Anti-patterns

The category collapses, each a wrong→right pair with the single feature that flips it. A test's kind is a claim; these are the ways the claim outruns the assertion. Lead with the right version; the wrong version exists to mark the trap.

### Circular golden
❌ Wrong:
```python
# scripts/gen_golden.py:  np.savez("golden/ecapa.npz", out=EcapaNumpy().embed(x, seed=42))
def test_exact_match():
    assert_allclose(EcapaNumpy().embed(x, seed=42), load("golden/ecapa.npz"), atol=0)  # docstring: "vs ONNX oracle"
```
✅ Right:
```python
@pytest.mark.regression  # honest: detects change, not correctness
def test_output_unchanged():
    assert_allclose(EcapaNumpy().embed(x, seed=42), load("golden/ecapa.npz"))
@pytest.mark.oracle
def test_matches_reference():          # the real correctness gate
    # Compare element-wise to the independent ONNX output with a tolerance that is the
    # numpy-vs-ONNX float divergence budget (fp32 accumulation order), not an eyeballed
    # cosine floor — a high cosine can still hide a per-dim bias a downstream stage sees.
    assert_allclose(EcapaNumpy().embed(x), onnx_reference.embed(x), atol=PORT_FP_BUDGET)
```
Why it flips: the golden was produced by the code under test, so the exact-match test can only detect change — the oracle claim requires an *independent* reference (the ONNX run), not the code's own captured output.
Prevents: a change-detector masquerading as a correctness proof, so a wrong-but-stable implementation passes forever.

### Conditional-guard can't-fail
❌ Wrong:
```python
def test_bootstrap_converges():
    bootstrap.run(scene)
    if bootstrap.phase >= EKF_TRACKING:      # skipped silently if it never converges
        assert bootstrap.geometry is not None
```
✅ Right:
```python
def test_bootstrap_converges():
    bootstrap.run(scene)
    assert bootstrap.phase >= EKF_TRACKING           # the precondition IS the claim
    assert position_error(bootstrap.geometry) < 0.05
```
Why it flips: the guarded condition *is* the behavior under test, so wrapping the assertions in `if precondition:` means the exact failure the test names — non-convergence — produces zero assertions and a green pass; asserting the precondition unconditionally makes it falsifiable. (Carve-out: guarding on a genuinely *environmental* precondition — hardware absent, optional dep missing — is legitimate, but express it as `pytest.skip(...)`, not a silent `if`, so a skip is visible where a guarded no-op is not.)
Prevents: false green on the specific behavior under test.

### In-test tautology
❌ Wrong:
```python
def test_tdoa_residual_zero():
    tdoa_obs = (d_b - d_a) / c
    residual = (d_b - d_a) / c - tdoa_obs      # x - x
    assert abs(residual) < 1e-9
```
✅ Right:
```python
def test_tdoa_matches_geometry():
    tdoa = estimate_tdoa(signal_a, signal_b)   # the real code
    assert abs(tdoa - (d_b - d_a) / c) < 1e-6  # expected from independent geometry
```
Why it flips: the discriminating feature is *independence of the compared-against value*, not merely "calls the code." The wrong version derives `expected` from the same expression as `actual` (so it would pass even if the estimator were called — `f(x) == f(x)` is also a tautology); the right version checks the estimator's output against a value derived independently, from geometry.
Prevents: a test that passes by construction and would survive deleting the entire module it names.

### Weakened-until-unfalsifiable
❌ Wrong:
```python
def test_localization_accuracy():
    az = localize(scene).azimuth
    assert 0 <= az < 360        # cannot fail — every azimuth is in range
```
✅ Right:
```python
def test_localization_accuracy():
    scene = scene_with_source_at(45.0, snr_db=20)
    az = localize(scene).azimuth
    # Tolerance derived, not eyeballed: the array's angular resolution at this aperture
    # and SNR (state the derivation in the docstring), so the bound is tight-to-the-floor
    # rather than a decorative "< 2.0".
    assert abs(az - 45.0) < expected_doa_resolution(scene)
```
Why it flips: the range `0 ≤ az < 360` is the definition of an azimuth, so it holds regardless of correctness; comparing to a *planted* 45° with a tolerance derived from the array's resolution is the accuracy claim the name makes.
Prevents: an "accuracy" test that a random-number generator would pass.

### Mock-shadow
❌ Wrong:
```python
def test_separates_sources():
    model = MagicMock(return_value=torch.randn(3, 16000))
    out = separate(audio, model)
    assert out.shape[0] == 3            # THE SMELL: asserts the mock's own configured shape
    model.assert_called_once()          # fine on its own (routing/contract) — NOT the smell here
```
✅ Right:
```python
def test_separates_sources():
    out = separate(two_speaker_mix, real_numpy_separator)   # real path
    # Source-separation output order is arbitrary (the BSS permutation problem), so score
    # under the best assignment — a fixed out[0]→ref_0 would flake on a CORRECT separator.
    best = max(mean_si_sdr(perm, refs) for perm in permutations(out))
    # Threshold anchored, not magic: require a stated margin over the unseparated mix
    # (the negative control), not an eyeballed dB. Both numbers live in the test's docstring.
    assert best > si_sdr_of_mix(refs) + MIN_SEPARATION_GAIN_DB
```
Why it flips: the wrong version's load-bearing assertion (`out.shape[0] == 3`) traces back to the value handed to the mock, so nothing real ran — note the `assert_called_once()` is *not* the defect (verifying a call happened is legitimate routing/contract). The right version drives the real separator, scores permutation-invariantly, and anchors the bar to a measured baseline.
Prevents: a green test over a component that was never executed — and, in the fix, a flaky test that fails on a correct-but-reordered separator or passes on an eyeballed threshold.

### Static-grep-as-behavior
❌ Wrong:
```python
def test_dsp_not_in_executor():
    src = Path("hub.py").read_text()
    assert not re.search(r"executor.*run_dsp", src)   # passes/fails on formatting
```
✅ Right:
```python
def test_dsp_runs_off_executor():
    with track_thread() as t:
        hub.process(chunk)
    assert t.dsp_thread != t.executor_thread          # observes real scheduling
# or: move the grep to a CI lint rule, not a behavioral test
```
Why it flips: scanning source text tests how the code is *written*, not what it *does* — a behavior-preserving refactor breaks it and a behavior-changing edit that keeps the string passes it; observing the actual thread tests the behavior.
Prevents: a "behavioral" test coupled to whitespace and identifier spelling.

### Oracle-name-on-smoke
❌ Wrong:
```python
def test_distinct_speakers_separated():
    ids = diarize(mix).speaker_ids
    assert len(ids) >= 1            # every non-empty diarization passes
```
✅ Right:
```python
def test_distinct_speakers_separated():
    ids = diarize(two_speaker_mix).speaker_ids
    assert len(set(ids)) == 2      # the separation claim the name makes
# or, if only liveness is intended, rename:
def test_diarize_smoke():
    assert diarize(mix) is not None
```
Why it flips: the name promises two speakers are told apart, but `len(ids) >= 1` holds for a single-speaker or even a broken result — the assertion must encode the discrimination the name claims, or the name must drop to `_smoke`.
Prevents: a coverage map that reads "separation: tested" when only liveness was checked.

### Episode-named file
❌ Wrong: `tests/test_wave1c_doa.py`, `tests/test_algorithmic_upgrades.py`, `tests/test_redteam_manifest_b1_b12.py` — files named after the development event, docstrings citing workstream IDs, coverage never folded into the subsystem suite.
✅ Right: `tests/unit/frontend/test_music.py`, `tests/unit/enhancement/test_separation.py` — files named after the source module they mirror; the episode's real tests migrated in under the right marker, its scaffolding deleted.
Why it flips: a filename keyed to *when* a test was written strands its coverage where no one maintaining the subsystem will look; a filename keyed to *what source it tests* keeps the suite navigable and dedup-able.
Prevents: migration scaffolding and one-off redteam passes petrifying into permanent, duplicated sediment.
