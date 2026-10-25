# Evaluation Report — Ghost Data Still Exists

## 1. Evaluation scope

The only available labelled evaluation set is the 32-row participant-facing `dataset/sample_deletion_requests.csv` paired with `dataset/sample_output.csv`. The 518-row `deletion_requests.csv` has no participant-visible canonical labels, so full-dataset hidden-answer accuracy cannot honestly be calculated. The sample output was used only by the evaluation routine; it is not imported by the prediction path and no sample case IDs or labels are hardcoded into `code/main.py`.

## 2. Public sample results

| Metric | Result |
|---|---:|
| Sample cases | 32 |
| Case-level deletion-status accuracy | **32 / 32 = 100.00%** |
| Exact ordered step-sequence accuracy | 11 / 32 = 34.38% |
| Step-position accuracy | 73.58% |
| Field-level accuracy | 85.06% |
| Sample cases with any exact-output mismatch | 21 / 32 |

Definitions:

- **Case-level status accuracy:** predicted `deletion_status` equals the sample label.
- **Exact sequence accuracy:** the entire ordered JSON array equals the sample answer, including every step field and evidence ID.
- **Step-position accuracy:** all six non-number step fields match at the same array position, divided by expected step positions.
- **Field-level accuracy:** correct values across the six evaluated step fields (`phase`, `system_id`, `resource_id`, `operation`, `state`, `evidence_id`), with missing predicted positions counted incorrect.

The first starter run scored 13/32 (40.63%) on status and 3/32 (9.38%) on exact sequence. The improvements focused on multilingual deletion intent, trace-ID grouping across log lines, whole-document PDF text matching, OCR resource-ID normalization, identity aliases and hashes, explicit policy-state interpretation, and tombstone redaction. The final run reached 32/32 status accuracy on the public sample.

## 3. Additional team-created evaluation cases

These are scenario-level tests created to exercise edge cases beyond simply replaying sample rows. They are implemented in `code/tests/test_agent.py` where applicable.

| Test ID | Scenario | Expected result | Validation |
|---|---|---|---|
| CUSTOM-01 | A customer asks for a copy of their data and explicitly says not to delete the account. | `NOT_APPLICABLE`, `[]` | Passed: explicit non-deletion intent overrides incidental wording. |
| CUSTOM-02 | The request uses an old email address that appears in `user_audit_log.csv`. | Resolve to the same stable `user_id` as the current identity. | Passed: historical email index resolves the identity. |
| CUSTOM-03 | A deleted-account tombstone still contains name, email, phone, and email hash. | `INCOMPLETE`; report exposed PII, redact tombstone, then verify redaction and retained security record. | Passed against the supplied tombstone fixture. |
| CUSTOM-04 | An integration connector is still enabled and can send customer data downstream. | `INCOMPLETE`; report active flow, disable it, then verify disabled state. | Passed against the supplied connector fixture. |
| CUSTOM-05 | A generated result contains valid operations but non-consecutive step numbers or an invalid phase. | Reject the result during contract validation. | Covered by step-contract assertions and output validator. |

Automated test command:

```bash
python -m unittest discover -s code/tests -v
```

Final unit-test result: **5 tests passed**.

## 4. Failures found and improvements made

1. **Intent detection was too narrow.** It missed completed-deletion follow-ups, “remove my profile” requests, and non-English requests. The phrase set was expanded and explicit access/correction/marketing opt-outs are handled as non-deletion requests.
2. **Multi-line traces lost subject-to-resource links.** A lookup email could be on a trace-start line while its resource ID appeared on a completion line. Lines are now joined by `trace_id` before matching.
3. **PDF extraction was line-local.** An attachment's resource reference and customer identity can be on different pages. PDF text is now preserved as a document-level artifact for matching.
4. **Screenshot resource IDs were inconsistently formatted.** OCR sometimes returned `data_flow.9846`; dotted resource IDs are normalized before matching.
5. **State parsing confused field names with values.** In particular, `enabled=false` could be misread as active. Connector state now uses the value of `enabled`, delivery status, and explicit state fields.
6. **Policy treatment was too coarse.** Shared support messages are redacted, subject-only attachments are deleted, analytics/telemetry are anonymized when attributable, and tombstones are redacted rather than deleted.
7. **Unknown/low-evidence cases could emit an empty INCOMPLETE plan.** These now receive a future account lookup verification step instead of an empty array. This is a planned check, not a claim that a record was observed.

## 5. Remaining limitations and next improvements

- Exact step-sequence accuracy is materially lower than status accuracy. Several public sample expected resource IDs are difficult to link uniquely from participant-visible artifacts, and some sample answers appear to rely on resources surfaced only in evidence captured after the case `audit_at`. The implementation follows the explicit point-in-time rule and does not use future evidence as proof.
- Some operational events contain no direct subject identifier. Current temporal resource correlation is deliberately narrow and should be replaced with stronger trace/request correlation if the organizer supplies a request-to-resource join key.
- OCR is best-effort and depends on the local Tesseract installation. For production, add image quality checks and retain OCR confidence and page coordinates.
- Next improvements: build a normalized evidence graph, retain provenance at field level, add a formal uncertainty state for unresolved identity links, and expand synthetic tests for backup restores, legal holds, cache copies, email delivery logs, and partial regional replica drift.

## 6. Reproducibility

The prediction pipeline reads participant-facing files under `dataset/` only. `sample_output.csv` is read only by `compare_sample()` for evaluation. Organizer-only truth, hidden labels, and generator internals are not used.
