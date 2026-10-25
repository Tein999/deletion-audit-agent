"""Find evidence linking analytics_1895 and analytics_5335 to users."""
import sys
sys.path.insert(0, 'D:/HackerRank/hackerrank-orchestrate-october26-main/code')
from pathlib import Path
import json, csv

ROOT = Path('D:/HackerRank/hackerrank-orchestrate-october26-main')
DATA = ROOT / 'dataset'
from main import Auditor, norm

a = Auditor(DATA)

# Search all evidence records for analytics_1895, analytics_5335, analytics_4566, analytics_4574, analytics_6077
target_resources = {'analytics_1895', 'analytics_5335', 'analytics_4566', 'analytics_4574', 'analytics_6077'}
print("=== Evidence records for anonymized analytics ===")
for r in a.evidence_records:
    if r.resource_id in target_resources:
        print(f"  {r.resource_id}: file_id={r.file_id}, sys={r.system_id}, cat={r.category}")
        print(f"    data={json.dumps(r.data)[:300]}")
        print()

# Look for user_21 aliases in ALL evidence
user21_aliases = a.aliases.get('user_21', set())
user25_aliases = a.aliases.get('user_25', set())
print(f"\nuser_21 aliases: {sorted(user21_aliases)}")
print(f"user_25 aliases: {sorted(user25_aliases)}")

# Check if any evidence file links analytics_5335 to any email/user
for r in a.evidence_records:
    if r.resource_id == 'analytics_5335':
        print(f"\nanalytics_5335 in {r.file_id}: data={json.dumps(r.data)[:500]}")
