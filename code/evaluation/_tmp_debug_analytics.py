"""Deep dive into case_21 and evidence_92 structure to understand why analytics_5335 is missed."""
import sys
sys.path.insert(0, 'D:/HackerRank/hackerrank-orchestrate-october26-main/code')
from pathlib import Path
import json, csv, re

ROOT = Path('D:/HackerRank/hackerrank-orchestrate-october26-main')
DATA = ROOT / 'dataset'
from main import Auditor, norm, iso, flatten, nonempty

a = Auditor(DATA)

# Check what's in evidence_92 for user_21
p92 = DATA / 'evidence/records/service_resource_export_20260915_114455.json'
data92 = json.loads(p92.read_text(encoding='utf-8'))
svc = data92.get('service_exports', {})

uid = 'user_21'
print(f"=== Evidence_92 records for {uid} ===")
for sysname, sysdata in svc.items():
    if isinstance(sysdata, dict):
        for subkey, subdata in sysdata.items():
            if isinstance(subdata, list):
                for item in subdata:
                    if any(str(v).casefold() == uid.casefold() for v in flatten(item).values() if nonempty(v)):
                        print(f"  {sysname}/{subkey}: {json.dumps(item)}")

# Check what evidence records exist for user_21  
uid_21 = 'user_21'
email_21 = 'amara-okeke@proton.me'
from main import value_set
aliases = set(a.aliases.get(uid_21, set()))
print(f"\n=== All evidence_92 records matched to user_21 ===")
ev92_recs = [r for r in a.evidence_records if r.file_id == 'evidence_92']
print(f"Total evidence_92 records: {len(ev92_recs)}")
for r in ev92_recs:
    matched = a._match_record(r, uid_21, aliases)
    if matched:
        print(f"  MATCH: resource={r.resource_id}, cat={r.category}")
    else:
        # Check why not matched
        vals = value_set(r.data)
        has_uid = norm(uid_21) in vals
        has_alias = bool(aliases & vals)
        # Check in text
        txt = r.text.casefold()
        print(f"  no-match: resource={r.resource_id}, cat={r.category}, has_uid={has_uid}, has_alias={has_alias}, data_vals={list(vals)[:5]}")

# Check specifically for analytics_5335
analytics_rec = next((r for r in a.evidence_records if r.resource_id == 'analytics_5335'), None)
if analytics_rec:
    print(f"\n=== analytics_5335 record ===")
    print(f"  file_id={analytics_rec.file_id}, sys={analytics_rec.system_id}, cat={analytics_rec.category}")
    print(f"  data={json.dumps(analytics_rec.data)[:500]}")
    print(f"  text={analytics_rec.text[:200]!r}")
    print(f"  values={value_set(analytics_rec.data)}")
    print(f"  aliases={aliases}")
    print(f"  match result: {a._match_record(analytics_rec, uid_21, aliases)}")
else:
    print("\nanalytics_5335 not found in evidence records!")
    # Check all analytics_* from evidence_92
    print("Analytics records from evidence_92:")
    for r in ev92_recs:
        if r.system_id == 'analytics_platform':
            print(f"  {r.resource_id}: data={json.dumps(r.data)[:200]}")
