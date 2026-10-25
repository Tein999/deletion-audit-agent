"""Contract and regression tests for the Ghost Data audit agent."""
import unittest
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from main import Auditor, PHASE_ORDER, OP_ORDER

class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = Auditor(ROOT / "dataset")
        import pandas as pd
        cls.sample_requests = pd.read_csv(ROOT / "dataset" / "sample_deletion_requests.csv", keep_default_na=False)

    def test_non_deletion_access_request_is_not_applicable(self):
        text = "Please send me a copy of my data. Do not delete my account."
        self.assertFalse(self.agent._request_authorizes_delete(text))

    def test_historical_email_resolves(self):
        row = self.agent.audit[self.agent.audit.field_name.astype(str).str.casefold() == "email"].iloc[0]
        self.assertEqual(self.agent.resolve(str(row.old_value)), str(row.user_id))

    def test_tombstone_policy_requires_redaction(self):
        request = self.sample_requests[self.sample_requests.email.astype(str).str.casefold() == "addo.kofi@gmail.com"].iloc[0]
        status, steps = self.agent.audit_case(request)
        self.assertEqual(status, "INCOMPLETE")
        self.assertTrue(any(s["operation"] == "REDACT_RECORD" and s["resource_id"] == "tombstone_9178" for s in steps))

    def test_active_connector_requires_disable(self):
        request = self.sample_requests[self.sample_requests.email.astype(str).str.casefold() == "lucia-torres@gmail.com"].iloc[0]
        status, steps = self.agent.audit_case(request)
        self.assertEqual(status, "INCOMPLETE")
        self.assertTrue(any(s["operation"] == "DISABLE_DATA_FLOW" for s in steps))

    def test_step_contract(self):
        request = self.agent.requests.iloc[0]
        _, steps = self.agent.audit_case(request)
        for i, step in enumerate(steps, 1):
            self.assertEqual(step["step_no"], i)
            self.assertIn(step["phase"], PHASE_ORDER)
            self.assertIn(step["operation"], OP_ORDER)
            self.assertEqual(set(step), {"step_no","phase","system_id","resource_id","operation","state","evidence_id"})

if __name__ == "__main__":
    unittest.main()
