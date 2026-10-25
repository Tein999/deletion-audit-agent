"""Inspect evidence files to understand account ID formats."""
import sys
sys.path.insert(0, 'D:/HackerRank/hackerrank-orchestrate-october26-main/code')
from pathlib import Path
import sqlite3, json, csv

ROOT = Path('D:/HackerRank/hackerrank-orchestrate-october26-main')
DATA = ROOT / 'dataset'

# Read sample deletion requests to know which users we're dealing with
sample_requests = list(csv.DictReader(open(DATA / 'sample_deletion_requests.csv', encoding='utf-8')))
sample_output = list(csv.DictReader(open(DATA / 'sample_output.csv', encoding='utf-8')))

# Parse expected outputs
for row in sample_output:
    row['steps'] = json.loads(row['steps_json'])

print("=== EXPECTED ACCOUNT RESOURCE IDs ===")
for row in sample_output[:10]:
    acct_steps = [s for s in row['steps'] if s['system_id'] == 'account_service']
    print(f"  {row['case_id']}: {[s['resource_id'] for s in acct_steps]}")

# Check evidence_54: customer_accounts_failover_replica
p54 = DATA / 'evidence/databases/customer_accounts_failover_replica_20260902.sql'
con = sqlite3.connect(':memory:')
con.executescript(p54.read_text(encoding='utf-8', errors='ignore'))
tables = [x[0] for x in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("\n=== evidence_54 tables:", tables)
for t in tables[:5]:
    cols = [x[1] for x in con.execute(f'PRAGMA table_info("{t}")')]
    print(f'  {t} cols:', cols)
    for row in con.execute(f'SELECT * FROM "{t}" LIMIT 3'):
        print('   ', dict(zip(cols, row)))
con.close()

# Check evidence_92: service_resource_export_20260915
p92 = DATA / 'evidence/records/service_resource_export_20260915_114455.json'
data92 = json.loads(p92.read_text(encoding='utf-8'))
print("\n=== evidence_92 structure:")
if isinstance(data92, list):
    print(f"  List of {len(data92)} items")
    for item in data92[:3]:
        print('  ', json.dumps(item)[:300])
elif isinstance(data92, dict):
    print("  Dict keys:", list(data92.keys())[:10])
    for k, v in list(data92.items())[:3]:
        print(f"  {k}:", str(v)[:200])
