"""Temporary probe: where do expected account_* IDs appear in evidence?"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dataset"

TARGETS = {
    "account_3960": "user_61",
    "account_5521": "user_50",
    "account_5037": "user_48",
    "account_6440": "user_21",
    "account_4990": "user_51",
    "account_3136": "user_25",
    "account_7012": "user_29",
    "account_4163": "user_30",
    "account_410": "user_23",
    "account_5684": "user_26",
    "account_3866": "user_27",
    "account_5482": "user_28",
    "account_4857": "user_541",
    "account_8858": "user_542",
}

idents = {}
with (DATA / "user_identities.csv").open(encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        idents[r["user_id"]] = r

aliases: dict[str, set[str]] = defaultdict(set)
for uid, r in idents.items():
    for k in ("name", "email", "phone", "email_hash", "user_id"):
        if r.get(k):
            aliases[uid].add(r[k].strip().casefold())

with (DATA / "user_audit_log.csv").open(encoding="utf-8-sig") as f:
    for a in csv.DictReader(f):
        uid = a["user_id"]
        for k in ("old_value", "new_value"):
            if a.get(k):
                aliases[uid].add(a[k].strip().casefold())

manifest = list(csv.DictReader((DATA / "evidence_files.csv").open(encoding="utf-8-sig")))

# Also scan activity for account resources linked somehow
activity = list(csv.DictReader((DATA / "system_activity.csv").open(encoding="utf-8-sig")))

for rid, uid in TARGETS.items():
    print("====", rid, uid)
    dotted = rid.replace("_", ".")
    found = 0
    for m in manifest:
        p = DATA / m["file_path"]
        if not p.exists() or p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if rid not in text and dotted not in text:
            continue
        als = [a for a in aliases[uid] if a and len(a) >= 5 and a in text.casefold()]
        print(
            f"  {m['file_id']} captured={m['captured_at']} "
            f"path={m['file_path']} aliases={als[:8]}"
        )
        idx = text.find(rid) if rid in text else text.find(dotted)
        if idx >= 0:
            ctx = text[max(0, idx - 100) : idx + 140].replace("\n", " | ")
            print("   ctx:", repr(ctx))
        found += 1
    # activity rows
    for a in activity:
        if a.get("resource_id") in {rid, dotted}:
            print(
                f"  ACTIVITY {a.get('activity_id')} sys={a.get('target_system')} "
                f"time={a.get('event_time')} result={a.get('reported_result')}"
            )
            found += 1
    if not found:
        print("  NOT FOUND")

# How does evidence_92 mention accounts?
print("\n==== evidence_92 / evidence_90 sample lines with account_")
for fid in ("evidence_92", "evidence_90", "evidence_51"):
    row = next((m for m in manifest if m["file_id"] == fid), None)
    if not row:
        print(fid, "missing")
        continue
    p = DATA / row["file_path"]
    print(fid, "->", row["file_path"], "captured", row["captured_at"])
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    accounts = sorted(set(re.findall(r"account[_.]\d+", text, re.I)))
    print("  account count", len(accounts), "sample", accounts[:20])
    # show first 3 account occurrences with nearby user/email
    for m in re.finditer(r"account[_.]\d+", text, re.I):
        ctx = text[max(0, m.start() - 120) : m.end() + 160].replace("\n", " | ")
        print("  HIT", m.group(0), ":", repr(ctx)[:240])
        if m.start() > 2000:
            break
