"""Inspect system_activity details for account resources used in samples."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dataset"

wanted = {
    "account_3960", "account_5521", "account_5037", "account_6440",
    "account_4990", "account_3136", "account_7012", "account_4163",
    "account_410", "account_5684", "account_3866", "account_5482",
    "account_4857", "account_8858",
}

with (DATA / "system_activity.csv").open(encoding="utf-8-sig") as f:
    for a in csv.DictReader(f):
        if a.get("resource_id") in wanted and a.get("target_system") == "account_service":
            print(a["activity_id"], a["resource_id"], a["event_time"], a["event_type"], a["reported_result"])
            print("  details:", a.get("details")[:400] if a.get("details") else None)

# Also check deletion request related activities - event types
print("\n=== event_type distribution for account_service ===")
from collections import Counter
c = Counter()
with (DATA / "system_activity.csv").open(encoding="utf-8-sig") as f:
    for a in csv.DictReader(f):
        if a.get("target_system") == "account_service":
            c[a.get("event_type")] += 1
print(c.most_common(20))

# Check if details ever contain emails / user ids
print("\n=== details containing @ or user_ ===")
n = 0
with (DATA / "system_activity.csv").open(encoding="utf-8-sig") as f:
    for a in csv.DictReader(f):
        d = a.get("details") or ""
        if "@" in d or "user_" in d:
            print(a["activity_id"], a["resource_id"], a["event_type"], d[:300])
            n += 1
            if n >= 15:
                break
print("shown", n)

# How does evidence_06 link account_3960 to user?
print("\n=== evidence_06 lines around account_3960 ===")
p = DATA / "evidence/logs/structured_service_events_eu_west_20260918.log"
text = p.read_text(encoding="utf-8", errors="ignore")
idx = text.find("account_3960")
print(repr(text[max(0, idx - 500): idx + 400]))

# Check customer_reference mapping in evidence_02
print("\n=== evidence_02 customer_reference -> resource_id ===")
p2 = DATA / "evidence/records/customer_data_snapshot_bundle_20260917.json"
obj = json.loads(p2.read_text(encoding="utf-8"))
stack = [obj]
while stack:
    cur = stack.pop()
    if isinstance(cur, dict):
        if cur.get("resource_id") and str(cur.get("resource_id")).startswith("account_"):
            print(cur.get("resource_id"), "ref=", cur.get("customer_reference") or cur.get("user_id"), "email=", cur.get("email"))
        stack.extend(cur.values())
    elif isinstance(cur, list):
        stack.extend(cur)
