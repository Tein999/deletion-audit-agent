"""Debug why account resource IDs are wrong."""
import sys
sys.path.insert(0, 'D:/HackerRank/hackerrank-orchestrate-october26-main/code')
from pathlib import Path
import json, csv, re

ROOT = Path('D:/HackerRank/hackerrank-orchestrate-october26-main')
DATA = ROOT / 'dataset'

# Load the auditor
from main import Auditor, norm, RESOURCE_ID_RE, iso

a = Auditor(DATA)

# Test case_09: expected account_3960, user_id=user_61, email=k.appiah88@gmail.com
def load_sample_row(case_id):
    for r in csv.DictReader(open(DATA / 'sample_deletion_requests.csv', encoding='utf-8')):
        if r['case_id'] == case_id:
            return r
    return None

email_09 = 'k.appiah88@gmail.com'
uid_09 = a.resolve(email_09)
print(f"case_09: email={email_09}, resolved_uid={uid_09}")
if uid_09:
    uid_num = re.search(r'(\d+)$', uid_09)
    derived = f"account_{int(uid_num.group(1)):03d}" if uid_num else None
    print(f"  Derived account (wrong): {derived}")
    
    sample_req = load_sample_row('case_09')
    audit_at = iso(sample_req['audit_at'])
    aliases = set(a.aliases.get(uid_09, set()))
    aliases.add(norm(email_09))
    matched = [r for r in a.evidence_records if r.time_ok(audit_at) and a._match_record(r, uid_09, aliases)]
    print(f"\n  Matched evidence records:")
    for r in matched:
        print(f"    file_id={r.file_id}, sys={r.system_id}, resource={r.resource_id}, cat={r.category}")
    
    # Check _account_absence
    result = a._account_absence(uid_09, audit_at)
    print(f"\n  _account_absence result: {result}")

# Test case_21: expected account_6440
email_21 = None
for r in csv.DictReader(open(DATA / 'sample_deletion_requests.csv', encoding='utf-8')):
    if r['case_id'] == 'case_21':
        email_21 = r['email']
        sample_req_21 = r
        break
uid_21 = a.resolve(email_21)
print(f"\ncase_21: email={email_21}, resolved_uid={uid_21}")
audit_at_21 = iso(sample_req_21['audit_at'])
aliases_21 = set(a.aliases.get(uid_21, set()))
aliases_21.add(norm(email_21))
matched_21 = [r for r in a.evidence_records if r.time_ok(audit_at_21) and a._match_record(r, uid_21, aliases_21)]
print(f"  Matched evidence records:")
for r in matched_21:
    print(f"    file_id={r.file_id}, sys={r.system_id}, resource={r.resource_id}, cat={r.category}")
result = a._account_absence(uid_21, audit_at_21)
print(f"  _account_absence result: {result}")

# Let's also check what the audit_case produces
st_21, steps_21 = a.audit_case(type('Row', (), sample_req_21)())
print(f"\n  Current prediction: {st_21}")
for s in steps_21:
    print(f"    {s}")
