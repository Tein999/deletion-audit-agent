# AI Interview Preparation — Ghost Data Still Exists

## 60-second explanation

“I built an offline-first deletion-audit agent that checks whether a deletion request is truly complete across primary and secondary systems. It resolves current and historical identifiers, extracts evidence from SQL snapshots, JSON exports, logs, PDFs, and screenshots, and reconstructs the state at the request's audit timestamp. A deterministic policy engine applies delete, redact, anonymize, retain, tombstone, sync-disable, and restore-block rules. It then emits the required ordered JSON steps in a validated CSV. I separated evidence extraction from policy decisions so an LLM cannot invent a deletion result or override retention requirements.”

## Architecture questions

**Why not trust the workflow status?**

Because `reported_status` and worker results are claims. The agent checks readback evidence and operational paths independently. A deletion is incomplete if a relevant copy remains, a sync can recreate it, or a backup can restore it.

**How do you resolve identity?**

Start with the request email, map it to the stable `user_id`, then gather current and historical values from `user_identities.csv` and `user_audit_log.csv`. Normalize case and whitespace, compute email hashes for historical/current emails, and use the full alias set to match downstream evidence. Prefer exact identity links over fuzzy name matches.

**How do you handle time?**

Each evidence item has a capture time and may have a record/event time. Both must be at or before `audit_at`. Later evidence must not change the point-in-time answer.

**How do you apply retention policy?**

The supplied policy determines treatment per category. Profiles, search entries, caches, exports, and marketing profiles are deleted. Shared support conversations are retained but redacted. Attributable analytics/telemetry is anonymized. Security and active legal-hold records are retained. A tombstone may retain only its stable internal user reference; direct identifiers are removed.

**How do you prevent hallucinated remediation?**

The model is not authoritative for final decisions. The pipeline uses fixed allowed operations/states, validates evidence references, numbers steps consecutively, and sorts by the required phase/operation/system/resource ordering.

## Evaluation discussion

The public sample achieved 100% deletion-status accuracy (32/32), 85.06% field accuracy, 73.58% step-position accuracy, and 34.38% exact ordered-sequence accuracy. The main remaining weakness is resource-level linkage for a subset of records where the evidence does not uniquely connect a resource to a subject or where the sample answer appears to reference post-audit evidence. I would improve this with an evidence graph and explicit provenance/confidence tracking rather than weakening the time cutoff.

## Connect to my experience

Use concrete examples from your own work when discussing implementation:

- Your Android internship used Clean Architecture/MVVM, Room, Flow/StateFlow, and repository-based unit testing. Relate this to separating ingestion, domain policy, and output layers.
- Your GenAI work integrated the OpenAI API and used prompt engineering with an offline fallback. Relate this to making model assistance optional while keeping core audit decisions deterministic.
- Your Python/Flask and REST API project work is relevant to evidence ingestion, parsing, and building a reproducible CLI/API around the audit engine.

## If asked what you would build next

1. Normalize every evidence item into a provenance-aware evidence graph.
2. Add per-field lineage for subject identifiers, resource IDs, and timestamps.
3. Use an LLM only for ambiguous unstructured extraction, with JSON schema validation and confidence thresholds.
4. Add replayable tests for restore races, delayed replicas, stale search indexes, legal holds, and identity changes.
5. Add an audit dashboard that explains every decision and exposes unresolved evidence gaps.
