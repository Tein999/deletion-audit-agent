"""Find identity->account links via traces, LINK_RESOURCE_IDENTITY, and catalogs."""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dataset"

# All LINK_RESOURCE_IDENTITY for account_*
print("=== LINK_RESOURCE_IDENTITY involving account_ ===")
with (DATA / "system_activity.csv").open(encoding="utf-8-sig") as f:
    for a in csv.DictReader(f):
        if a.get("event_type") != "LINK_RESOURCE_IDENTITY":
            continue
        d = a.get("details") or ""
        if "account_" in d or str(a.get("resource_id", "")).startswith("account"):
            print(a["activity_id"], a["resource_id"], d)

# Trace around account_3960 in evidence_06
print("\n=== evidence_06 trace tr-1463969 ===")
p = DATA / "evidence/logs/structured_service_events_eu_west_20260918.log"
text = p.read_text(encoding="utf-8", errors="ignore")
# find all lines with that trace
for line in text.splitlines():
    if "tr-1463969" in line or ("account_3960" in line):
        print(line[:300])

# Search all logs for email k.appiah88 near account
print("\n=== search all text evidence for k.appiah88 ===")
manifest = list(csv.DictReader((DATA / "evidence_files.csv").open(encoding="utf-8-sig")))
for m in manifest:
    path = DATA / m["file_path"]
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf"}:
        continue
    if not path.exists():
        continue
    try:
        t = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    if "k.appiah88@gmail.com" not in t.casefold() and "user_61" not in t.casefold():
        continue
    print(m["file_id"], m["file_path"])
    # extract account ids in same file
    accounts = sorted(set(re.findall(r"account_\d+", t)))
    print("  accounts in file:", accounts[:30], "count", len(accounts))
    # show lines with email or user_61
    for line in t.splitlines():
        lc = line.casefold()
        if "k.appiah88" in lc or "user_61" in lc:
            print("  LINE:", line[:350])

# How current auditor matches evidence_06 to user_61
print("\n=== Does evidence_06 contain both email and account on same record? ===")
# The earlier probe said aliases in file - meaning whole file has both
# Check line-level co-occurrence via trace
from collections import defaultdict
trace_lines = defaultdict(list)
for line in text.splitlines():
    tm = re.search(r'"trace_id":"([^"]+)"', line) or re.search(r"trace_id=([^\s,|]+)", line)
    if tm:
        trace_lines[tm.group(1)].append(line)
for tid, lines in trace_lines.items():
    joined = "\n".join(lines).casefold()
    if "account_3960" in joined or "k.appiah88" in joined or "user_61" in joined:
        if "account_3960" in joined and ("k.appiah88" in joined or "user_61" in joined):
            print("JOINED TRACE", tid)
            for L in lines:
                print(" ", L[:250])
