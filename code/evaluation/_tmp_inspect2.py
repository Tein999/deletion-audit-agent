"""Deeper inspection of evidence_92 and identify account_id extraction patterns."""
from pathlib import Path
import json, csv, re

ROOT = Path('D:/HackerRank/hackerrank-orchestrate-october26-main')
DATA = ROOT / 'dataset'

# evidence_92: service_resource_export_20260915
p92 = DATA / 'evidence/records/service_resource_export_20260915_114455.json'
data92 = json.loads(p92.read_text(encoding='utf-8'))
print("=== evidence_92 keys:", list(data92.keys()))
svc = data92.get('service_exports', {})
print("  service_export systems:", list(svc.keys()))
for sysname, sysdata in svc.items():
    print(f"\n  === {sysname} ===")
    if isinstance(sysdata, dict):
        for subkey, subdata in sysdata.items():
            if isinstance(subdata, list):
                print(f"    {subkey}: {len(subdata)} items")
                for item in subdata[:2]:
                    print("     ", json.dumps(item)[:300])
            else:
                print(f"    {subkey}:", str(subdata)[:100])

# Now look at the sample users and their expected account IDs
print("\n=== SAMPLE USER EMAILS AND EXPECTED ACCOUNT IDs ===")
sample_requests = list(csv.DictReader(open(DATA / 'sample_deletion_requests.csv', encoding='utf-8')))
sample_output = list(csv.DictReader(open(DATA / 'sample_output.csv', encoding='utf-8')))
identities = list(csv.DictReader(open(DATA / 'user_identities.csv', encoding='utf-8')))
id_by_email = {}
for r in identities:
    id_by_email[r['email'].strip().casefold()] = r
    
for row in sample_requests[:10]:
    email = row['email'].strip().casefold()
    uid = id_by_email.get(email, {}).get('user_id', 'UNKNOWN')
    expected = next((o for o in sample_output if o['case_id'] == row['case_id']), None)
    steps = json.loads(expected['steps_json']) if expected else []
    acct = next((s['resource_id'] for s in steps if s['system_id'] == 'account_service'), 'NONE')
    print(f"  {row['case_id']}: email={email}, user_id={uid}, expected_account={acct}")
