"""Analyze expected step ordering patterns from sample_output.csv to determine correct sort keys."""
from pathlib import Path
import json, csv

ROOT = Path('D:/HackerRank/hackerrank-orchestrate-october26-main')
DATA = ROOT / 'dataset'

sample_output = list(csv.DictReader(open(DATA / 'sample_output.csv', encoding='utf-8')))

SYSTEM_ORDER = {}
# Collect system ordering from all verification phases
for row in sample_output:
    steps = json.loads(row['steps_json'])
    ver_steps = [s for s in steps if s['phase'] == 'VERIFICATION']
    for i, s in enumerate(ver_steps):
        sys = s['system_id']
        op = s['operation']
        if sys not in SYSTEM_ORDER:
            SYSTEM_ORDER[sys] = set()
        SYSTEM_ORDER[sys].add(i)

print("=== SYSTEM POSITION DISTRIBUTIONS IN VERIFICATION ===")
for sys, positions in sorted(SYSTEM_ORDER.items()):
    avg = sum(positions) / len(positions)
    print(f"  {sys}: positions={sorted(positions)}, avg={avg:.1f}")

print("\n=== OPERATION ORDER WITHIN EACH PHASE ===")
# Look at finding ordering 
for row in sample_output:
    steps = json.loads(row['steps_json'])
    findings = [s for s in steps if s['phase'] == 'FINDING']
    if len(findings) > 1:
        print(f"\n  {row['case_id']} findings:")
        for s in findings:
            print(f"    {s['step_no']}: {s['operation']} / {s['system_id']} / {s['resource_id']}")
        rems = [s for s in steps if s['phase'] == 'REMEDIATION']
        print(f"  {row['case_id']} remediations:")
        for s in rems:
            print(f"    {s['step_no']}: {s['operation']} / {s['system_id']} / {s['resource_id']}")

# System ordering for verification
print("\n=== VERIFICATION SYSTEM ORDERING ===")
VERIF_SYSTEM_ORDER = {
    'account_service': 1, 'search_service': 2, 'export_service': 2, 'support_platform': 3,
    'security_service': 4, 'analytics_platform': 5, 'identity_service': 5,
    'integration_service': 6, 'backup_service': 7, 'marketing_service': 8,
    'notification_service': 8, 'cache_service': 8,
}
for row in sample_output:
    steps = json.loads(row['steps_json'])
    ver_steps = [s for s in steps if s['phase'] == 'VERIFICATION']
    if len(ver_steps) > 1:
        print(f"\n  {row['case_id']} [{row['deletion_status']}]:")
        for s in ver_steps:
            print(f"    {s['step_no']}: op={s['operation']}, sys={s['system_id']}, res={s['resource_id']}")
