"""Inspect evidence_92 analytics section closely."""
from pathlib import Path
import json

ROOT = Path('D:/HackerRank/hackerrank-orchestrate-october26-main')
DATA = ROOT / 'dataset'

p92 = DATA / 'evidence/records/service_resource_export_20260915_114455.json'
data92 = json.loads(p92.read_text(encoding='utf-8'))
svc = data92.get('service_exports', {})

# Full analytics section
print("=== analytics_platform full ===")
print(json.dumps(svc.get('analytics_platform', {}), indent=2))

print("\n=== account_service full ===")
print(json.dumps(svc.get('account_service', {}), indent=2))

print("\n=== security_service full ===")
print(json.dumps(svc.get('security_service', {}), indent=2))
