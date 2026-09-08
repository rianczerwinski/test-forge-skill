# Worked example — capability decision and grouping potency

## Input

“Can this pipeline distinguish the speakers in an ordinary single-microphone recording? If it works, we will survey microphone/session variation.”

## Decision gate

Select a bounded initial case with independently labeled speaker segments and conditions that actually contain the discrimination problem. State why those conditions are informative. Include the necessary recording duration and setup cost in an initial estimate; measure a small throughput sample before committing to the expensive remainder.

- Pass: the chosen case meets the sourced grouping criterion; proceed to designing the population survey.
- Fail: the basic path violates the criterion; stop the survey and diagnose with the retained inputs/results.
- Inconclusive: bad labels, missing speakers, environmental failure, or insufficient discriminatory content; repair or expand only the relevant condition.

Set the case count and quality criterion from this decision and evidence needs. A successful capability case establishes demonstrated behavior under its conditions, not reliability across microphones or sessions. Reuse an identical completed case in the later stage when code/configuration/input identities remain compatible.

## Potent assertion

For a tiny exact fixture with known segment alignment, compare the partition of segments rather than numerical label names:

```python
def assert_same_partition(actual, truth):
    assert len(actual) == len(truth)
    for i in range(len(truth)):
        for j in range(i):
            assert (actual[i] == actual[j]) == (truth[i] == truth[j])


truth = ["A", "A", "B", "A", "B", "B"]
assert_same_partition([7, 7, 9, 7, 9, 9], truth)
assert_same_partition([9, 9, 7, 9, 7, 7], truth)
```

This fixture accepts arbitrary relabeling while rejecting a single-speaker collapse or alternating labels. The pairwise comparison is deliberately small and transparent, not a production-scale scoring recommendation. Real diarization needs a sourced alignment/error metric and appropriate allowance for uncertain boundaries or labels.

## Potency trace

The independently labeled fixture contains both speakers repeatedly. The actual grouping path processes it; no mock supplies the answer. Wrong grouping propagates into the segment labels and the partition assertion rejects it. Permuting correct label names leaves the test green.

Exercise incorrect outputs such as all-one labels, alternating labels, and missing segments against the assertion, then exercise an actual grouping defect through the system when claiming end-to-end detection. Label the former oracle discrimination and the latter system detection; neither substitutes for the other.
