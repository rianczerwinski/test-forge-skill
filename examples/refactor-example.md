# Worked example — proof-obligation-driven apparatus refactor

This example continues the embedding-server audit in [audit-example.md](audit-example.md). The refactor’s target was not a smaller suite; it was a denser and more reachable system of proof.

## Governing invariant

Every retained cost must buy a named failure signal. Every removed test must be dominated on claim, authority, seam, cadence, and falsification role—not merely duplicate line coverage.

## Choice ledger

| Choice | Evidence and reasoning | Rejected alternative | Validation |
|---|---|---|---|
| Keep HTTP matrices on the real application with a deterministic model. | Validation, CORS, schemas, counters, and error envelopes are decided outside model numerics. | Replay the same matrix through a downloaded model for realism. | The changed HTTP/client cluster passed at routine cadence; the real-model layer retained one native/v2 seam case. |
| Cross real TCP for client and third-party compatibility. | In-process clients bypass serialization and socket failures. | Use the framework test client for everything. | Python client tests ran against an already-bound uvicorn socket; the bound socket removed free-port races. |
| Load the locked model once and batch compatible numeric claims. | Shape, finiteness, normalization, and semantic relations require real inference but not separate model loads. | One isolated forward per assertion. | The model module fell from 253.37 seconds to 24.06 seconds while retaining the same authorities. |
| Use the real tokenizer but substitute neural forward for the exact context boundary. | Token admission is decided after tokenization and before inference. | Infer at maximum context on both sides of the boundary. | A temporary `>`→`>=` mutation made the exact 8,192-token case fail. |
| Replace fixed sleeps with events and fake clocks. | The old tests paid planted delays in teardown and introduced scheduling races. | Shorten the sleeps. | Timeout paths still executed while individual calls fell to roughly 0.11 seconds. |
| Extract a controlled pure wheel and launch a fresh interpreter. | The claim was wheel-content discovery without checkout leakage, not pip behavior. | Create a venv and run pip for every case. | Fresh-process conformance remained intact and the test call fell to 0.36 seconds. |
| Make every nonroutine selector explicit. | Default `not slow` configuration persisted even when lifecycle files were named. | Trust file naming and job titles. | Removing `-m slow` temporarily was rejected by a workflow regression. |

## Consolidation

Shared application and real-socket fixtures replaced divergent module-local copies. The 31-case slow server matrix became two irreducible real-model HTTP tests. Compatible assertions shared setup or batches; failures remained individually diagnostic. The 100-request concurrency regression stayed because no cheaper evidence observed its lost-counter failure.

No wholesale test-tree move was performed. Stable ownership was already legible, and a claim-to-evidence map supplied navigation without source-mirroring churn.

## Reachability repair

The apparatus documented exact routine, acceptance, real-model, numeric-parity, lifecycle, and publication commands. Scheduled CI installed the necessary dependency groups and explicitly selected slow evidence. Local absence of platform or optional dependencies remained a proof limit rather than being counted as success.

## Closure evidence

- Routine plane: 537 passed, 2 optional modules skipped, 18 slow tests deselected, no warnings, 20.13 seconds.
- Irreducible real-model plane: 7 passed in 17.61 seconds with one shared model load.
- Claim mutations: the inclusive token-boundary error and removed lifecycle selector were both rejected.
- Mechanical smell scan: no remaining candidates, explicitly treated as supporting evidence rather than an all-clear.
- Production source: unchanged.

The refactor added routine real-TCP coverage while becoming faster. That is evidence density: fewer broad repetitions, more exact boundaries, and no hidden claim that every environment ran locally.
