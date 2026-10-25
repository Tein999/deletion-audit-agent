# Token Usage and Cost Report

## Final full-dataset run

| Item | Value |
|---|---:|
| Run date | 2026-10-25 |
| Input requests | 518 |
| Model provider | None — local deterministic pipeline |
| Model name | None — no external LLM invoked |
| External model calls | 0 |
| Input tokens | 0 |
| Output tokens | 0 |
| Total tokens | 0 |
| Average tokens per request | 0.00 |
| Estimated total model cost | USD $0.00 |
| Estimated cost per request | USD $0.000000 |
| Full run elapsed time | 25.21 seconds |

## Per-model breakdown

No external model was called during the final full-dataset run. Therefore there are no per-provider or per-model token/cost subtotals. Python, Pandas, SQLite, PDF text extraction, and optional local OCR are not LLM providers and do not consume model tokens.

## Accounting method

- Model-call count and token totals are zero because `code/main.py` performs deterministic local parsing, identity resolution, policy evaluation, state reconstruction, and output validation.
- No API key, paid model endpoint, or remote inference service was used.
- Estimated model cost is zero. Local CPU/runtime cost is not included because no billing rate was supplied.
- `code/prompts/evidence_interpretation.md` is an optional prompt specification only; it was not sent to a model in this run.

This report describes the actual run that produced the submitted root-level `output.csv`; it does not estimate hypothetical future LLM usage.
