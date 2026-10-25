"""Probe how account resources link to users via evidence + activity."""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dataset"


def iso(v):
    if not v:
        return None
    d = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


# Load sample requests for failing cases
cases = [
    "case_09", "case_18", "case_20", "case_21", "case_22", "case_23",
    "case_25", "case_26", "case_27", "case_28", "case_29", "case_30",
    "case_31", "case_32",
]
reqs = {}
with (DATA / "sample_deletion_requests.csv").open(encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        if r["case_id"] in cases:
            reqs[r["case_id"]] = r

idents = {}
email_to_uid = {}
with (DATA / "user_identities.csv").open(encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        idents[r["user_id"]] = r
        email_to_uid[r["email"].strip().casefold()] = r["user_id"]

with (DATA / "user_audit_log.csv").open(encoding="utf-8-sig") as f:
    for a in csv.DictReader(f):
        if a["field_name"].lower() == "email":
            for k in ("old_value", "new_value"):
                if a.get(k):
                    email_to_uid.setdefault(a[k].strip().casefold(), a["user_id"])

activity = list(csv.DictReader((DATA / "system_activity.csv").open(encoding="utf-8-sig")))

# Inspect evidence_92 account entries fully
p = DATA / "evidence/records/service_resource_export_20260915_114455.json"
obj = json.loads(p.read_text(encoding="utf-8"))
print("=== evidence_92 account lookups ===")
lookups = obj.get("account_service", {}).get("lookups") or obj.get("account_service", {}).get("profiles") or []
# walk
stack = [obj]
while stack:
    cur = stack.pop()
    if isinstance(cur, dict):
        rid = cur.get("resource_id")
        if isinstance(rid, str) and rid.startswith("account_"):
            print(json.dumps(cur, indent=2)[:500])
            print("---")
        stack.extend(cur.values())
    elif isinstance(cur, list):
        stack.extend(cur)

print("\n=== per-case: activity account events near request/report/audit ===")
for cid in cases:
    row = reqs[cid]
    email = row["email"].strip().casefold()
    uid = email_to_uid.get(email)
    requested = iso(row["requested_at"])
    reported = iso(row["reported_at"])
    audit_at = iso(row["audit_at"])
    print(f"\n{cid} uid={uid} email={email}")
    print(f"  requested={requested} reported={reported} audit_at={audit_at}")
    # account_service activities before audit_at
    hits = []
    for a in activity:
        if a.get("target_system") != "account_service":
            continue
        et = iso(a.get("event_time"))
        if not et or et > audit_at:
            continue
        rid = a.get("resource_id", "")
        if not str(rid).startswith("account"):
            continue
        # temporal proximity to reported/requested
        delta_rep = abs((et - reported).total_seconds()) if reported else None
        delta_req = abs((et - requested).total_seconds()) if requested else None
        hits.append((delta_rep or 1e18, delta_req or 1e18, et, a.get("activity_id"), rid, a.get("reported_result"), a.get("operation")))
    hits.sort()
    print("  closest account activities:")
    for h in hits[:5]:
        print("   ", h)

# Also check if activity details contain emails
print("\n=== sample activity columns ===")
print(list(activity[0].keys()) if activity else None)
# find any activity with user email in any field
sample_email = reqs["case_21"]["email"].casefold()
for a in activity:
    blob = " ".join(str(v) for v in a.values()).casefold()
    if sample_email in blob or "user_21" in blob:
        print("activity linked to case_21:", a)
        break
else:
    print("No activity row contains case_21 email/user_id")
