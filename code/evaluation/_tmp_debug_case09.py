"""Debug why case_09 uses invented account_061 instead of account_3960."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from main import Auditor  # noqa: E402

a = Auditor(ROOT / "dataset")
req = a.requests  # full set; use sample
import pandas as pd

sample = pd.read_csv(ROOT / "dataset" / "sample_deletion_requests.csv", keep_default_na=False)
row = next(r for r in sample.itertuples(index=False) if r.case_id == "case_09")
print("email", row.email, "audit_at", row.audit_at)
uid = a.resolve(row.email)
print("uid", uid)
aliases = set(a.aliases.get(uid, set()))
aliases.add(row.email.strip().casefold())
print("aliases sample", sorted(aliases)[:10])

from main import iso

audit_at = iso(row.audit_at)
matched = [r for r in a.evidence_records if r.time_ok(audit_at) and a._match_record(r, uid, aliases)]
print("matched count", len(matched))
for r in matched:
    if "account" in r.resource_id or r.category == "USER_PROFILE":
        print(
            "REC", r.file_id, r.resource_id, r.category, r.system_id,
            "cap", r.captured_at, "rt", r.record_time,
            "status", a._status_text(r)[:80],
            "keys", list(r.data.keys())[:12],
        )
        print("  text snippet:", (r.text or "")[:200].replace("\n", " | "))

status, steps = a.audit_case(row)
print("STATUS", status)
print(json.dumps(steps, indent=2))

# Is account_3960 in evidence_records at all?
hits = [r for r in a.evidence_records if r.resource_id == "account_3960"]
print("\naccount_3960 evidence records:", len(hits))
for r in hits:
    print(r.file_id, r.category, r.system_id, r.captured_at, r.record_time, "time_ok", r.time_ok(audit_at))
    print("  match?", a._match_record(r, uid, aliases))
    print("  data", {k: r.data.get(k) for k in list(r.data)[:15]})
    print("  text", (r.text or "")[:300].replace("\n", " | "))
