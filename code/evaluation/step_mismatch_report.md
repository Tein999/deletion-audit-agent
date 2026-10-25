# Sample Output Diagnostic Report

- Expected cases: 32
- Predicted cases: 32
## Metrics
- Status accuracy: 32/32 = 100.00%
- Exact sequence accuracy: 12/32 = 37.50%
- Step-position accuracy: 147/183 = 80.33%
- Field accuracy: 1188/1281 = 92.74%
- Missing predicted cases: 0
- Unexpected predicted cases: 0


## case_01
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 1; predicted steps: 1
- Step 1 mismatch:
  - evidence_id: expected `evidence_54`; predicted `evidence_87`

## case_02
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 1; predicted steps: 1
- Step 1 mismatch:
  - evidence_id: expected `evidence_54`; predicted `evidence_87`

## case_03
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 3; predicted steps: 3
- Step 3 mismatch:
  - resource_id: expected `analytics_9406`; predicted `analytics_5589`

## case_04
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 2; predicted steps: 2
- Step 1 mismatch:
  - evidence_id: expected `evidence_54`; predicted `evidence_90`

## case_05
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_06
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_07
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_08
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_09
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 5; predicted steps: 4
- Step 3 mismatch:
  - resource_id: expected `account_3960`; predicted `account_061`
- Step 4 mismatch:
  - system_id: expected `security_service`; predicted `backup_service`
  - resource_id: expected `audit_record_4902`; predicted `backup_4978`
  - operation: expected `VERIFY_RECORD_PRESENT`; predicted `VERIFY_RESTORE_BLOCKED`
  - state: expected `PRESENT`; predicted `BLOCKED`
- Missing predicted step 5: `{"step_no": 5, "phase": "VERIFICATION", "system_id": "backup_service", "resource_id": "backup_4978", "operation": "VERIFY_RESTORE_BLOCKED", "state": "BLOCKED", "evidence_id": ""}`

## case_10
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_11
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_12
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_13
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_14
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_15
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_16
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_17
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 5; predicted steps: 6
- Step 4 mismatch:
  - system_id: expected `security_service`; predicted `account_service`
  - resource_id: expected `audit_record_1797`; predicted `account_6523`
  - operation: expected `VERIFY_RECORD_PRESENT`; predicted `VERIFY_RECORD_ABSENT`
  - state: expected `PRESENT`; predicted `ABSENT`
- Step 5 mismatch:
  - system_id: expected `backup_service`; predicted `security_service`
  - resource_id: expected `backup_3245`; predicted `audit_record_1797`
  - operation: expected `VERIFY_RESTORE_BLOCKED`; predicted `VERIFY_RECORD_PRESENT`
  - state: expected `BLOCKED`; predicted `PRESENT`
- Extra predicted step 6: `{"step_no": 6, "phase": "VERIFICATION", "system_id": "backup_service", "resource_id": "backup_3245", "operation": "VERIFY_RESTORE_BLOCKED", "state": "BLOCKED", "evidence_id": ""}`

## case_18
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 14; predicted steps: 13
- Step 9 mismatch:
  - resource_id: expected `account_5521`; predicted `account_050`
- Step 11 mismatch:
  - system_id: expected `security_service`; predicted `support_platform`
  - resource_id: expected `audit_record_6645`; predicted `support_5569`
  - operation: expected `VERIFY_RECORD_PRESENT`; predicted `VERIFY_RECORD_REDACTED`
  - state: expected `PRESENT`; predicted `REDACTED`
- Step 12 mismatch:
  - system_id: expected `support_platform`; predicted `analytics_platform`
  - resource_id: expected `support_5569`; predicted `analytics_037`
  - operation: expected `VERIFY_RECORD_REDACTED`; predicted `VERIFY_RECORD_ANONYMIZED`
  - state: expected `REDACTED`; predicted `ANONYMIZED`
- Step 13 mismatch:
  - system_id: expected `analytics_platform`; predicted `integration_service`
  - resource_id: expected `analytics_037`; predicted `data_flow_4890`
  - operation: expected `VERIFY_RECORD_ANONYMIZED`; predicted `VERIFY_DATA_FLOW_DISABLED`
  - state: expected `ANONYMIZED`; predicted `DISABLED`
- Missing predicted step 14: `{"step_no": 14, "phase": "VERIFICATION", "system_id": "integration_service", "resource_id": "data_flow_4890", "operation": "VERIFY_DATA_FLOW_DISABLED", "state": "DISABLED", "evidence_id": ""}`

## case_19
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Step sequence: exact match

## case_20
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 8; predicted steps: 7
- Step 5 mismatch:
  - resource_id: expected `account_5037`; predicted `account_048`
- Step 7 mismatch:
  - system_id: expected `security_service`; predicted `integration_service`
  - resource_id: expected `audit_record_5569`; predicted `data_flow_1770`
  - operation: expected `VERIFY_RECORD_PRESENT`; predicted `VERIFY_DATA_FLOW_DISABLED`
  - state: expected `PRESENT`; predicted `DISABLED`
- Missing predicted step 8: `{"step_no": 8, "phase": "VERIFICATION", "system_id": "integration_service", "resource_id": "data_flow_1770", "operation": "VERIFY_DATA_FLOW_DISABLED", "state": "DISABLED", "evidence_id": ""}`

## case_21
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 3; predicted steps: 2
- Step 1 mismatch:
  - resource_id: expected `account_6440`; predicted `account_021`
  - evidence_id: expected `evidence_92`; predicted `evidence_90`
- Missing predicted step 3: `{"step_no": 3, "phase": "VERIFICATION", "system_id": "analytics_platform", "resource_id": "analytics_5335", "operation": "VERIFY_RECORD_ANONYMIZED", "state": "ANONYMIZED", "evidence_id": "evidence_92"}`

## case_22
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 8; predicted steps: 8
- Step 5 mismatch:
  - resource_id: expected `account_4990`; predicted `account_051`

## case_23
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 8; predicted steps: 7
- Step 5 mismatch:
  - resource_id: expected `account_410`; predicted `account_023`
- Missing predicted step 8: `{"step_no": 8, "phase": "VERIFICATION", "system_id": "security_service", "resource_id": "audit_record_4128", "operation": "VERIFY_RECORD_PRESENT", "state": "PRESENT", "evidence_id": ""}`

## case_24
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 7; predicted steps: 6
- Missing predicted step 7: `{"step_no": 7, "phase": "VERIFICATION", "system_id": "security_service", "resource_id": "audit_record_7095", "operation": "VERIFY_RECORD_PRESENT", "state": "PRESENT", "evidence_id": ""}`

## case_25
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 3; predicted steps: 3
- Step 1 mismatch:
  - resource_id: expected `account_3136`; predicted `account_025`
  - evidence_id: expected `evidence_92`; predicted `evidence_90`
- Step 3 mismatch:
  - resource_id: expected `analytics_1895`; predicted `analytics_4566`

## case_26
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 6; predicted steps: 6
- Step 1 mismatch:
  - resource_id: expected `account_5684`; predicted `account_026`
  - evidence_id: expected `evidence_92`; predicted `evidence_90`

## case_27
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 6; predicted steps: 5
- Step 1 mismatch:
  - resource_id: expected `account_3866`; predicted `account_027`
  - evidence_id: expected `evidence_92`; predicted `evidence_90`
- Step 4 mismatch:
  - system_id: expected `analytics_platform`; predicted `integration_service`
  - resource_id: expected `analytics_4574`; predicted `data_flow_2295`
  - operation: expected `VERIFY_RECORD_ANONYMIZED`; predicted `VERIFY_DATA_FLOW_DISABLED`
  - state: expected `ANONYMIZED`; predicted `DISABLED`
- Step 5 mismatch:
  - system_id: expected `integration_service`; predicted `backup_service`
  - resource_id: expected `data_flow_2295`; predicted `backup_5970`
  - operation: expected `VERIFY_DATA_FLOW_DISABLED`; predicted `VERIFY_RESTORE_BLOCKED`
  - state: expected `DISABLED`; predicted `BLOCKED`
- Missing predicted step 6: `{"step_no": 6, "phase": "VERIFICATION", "system_id": "backup_service", "resource_id": "backup_5970", "operation": "VERIFY_RESTORE_BLOCKED", "state": "BLOCKED", "evidence_id": "evidence_92"}`

## case_28
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 6; predicted steps: 5
- Step 1 mismatch:
  - resource_id: expected `account_5482`; predicted `account_028`
  - evidence_id: expected `evidence_92`; predicted `evidence_90`
- Step 4 mismatch:
  - system_id: expected `analytics_platform`; predicted `integration_service`
  - resource_id: expected `analytics_6077`; predicted `data_flow_2337`
  - operation: expected `VERIFY_RECORD_ANONYMIZED`; predicted `VERIFY_DATA_FLOW_DISABLED`
  - state: expected `ANONYMIZED`; predicted `DISABLED`
- Step 5 mismatch:
  - system_id: expected `integration_service`; predicted `backup_service`
  - resource_id: expected `data_flow_2337`; predicted `backup_838`
  - operation: expected `VERIFY_DATA_FLOW_DISABLED`; predicted `VERIFY_RESTORE_BLOCKED`
  - state: expected `DISABLED`; predicted `BLOCKED`
- Missing predicted step 6: `{"step_no": 6, "phase": "VERIFICATION", "system_id": "backup_service", "resource_id": "backup_838", "operation": "VERIFY_RESTORE_BLOCKED", "state": "BLOCKED", "evidence_id": "evidence_92"}`

## case_29
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 14; predicted steps: 13
- Step 9 mismatch:
  - resource_id: expected `account_7012`; predicted `account_029`
- Step 11 mismatch:
  - system_id: expected `security_service`; predicted `support_platform`
  - resource_id: expected `audit_record_3954`; predicted `support_5281`
  - operation: expected `VERIFY_RECORD_PRESENT`; predicted `VERIFY_RECORD_REDACTED`
  - state: expected `PRESENT`; predicted `REDACTED`
- Step 12 mismatch:
  - system_id: expected `support_platform`; predicted `analytics_platform`
  - resource_id: expected `support_5281`; predicted `analytics_5208`
  - operation: expected `VERIFY_RECORD_REDACTED`; predicted `VERIFY_RECORD_ANONYMIZED`
  - state: expected `REDACTED`; predicted `ANONYMIZED`
- Step 13 mismatch:
  - system_id: expected `analytics_platform`; predicted `integration_service`
  - resource_id: expected `analytics_5208`; predicted `data_flow_3827`
  - operation: expected `VERIFY_RECORD_ANONYMIZED`; predicted `VERIFY_DATA_FLOW_DISABLED`
  - state: expected `ANONYMIZED`; predicted `DISABLED`
- Missing predicted step 14: `{"step_no": 14, "phase": "VERIFICATION", "system_id": "integration_service", "resource_id": "data_flow_3827", "operation": "VERIFY_DATA_FLOW_DISABLED", "state": "DISABLED", "evidence_id": ""}`

## case_30
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 14; predicted steps: 13
- Step 9 mismatch:
  - resource_id: expected `account_4163`; predicted `account_030`
- Step 11 mismatch:
  - system_id: expected `security_service`; predicted `support_platform`
  - resource_id: expected `audit_record_1707`; predicted `support_6477`
  - operation: expected `VERIFY_RECORD_PRESENT`; predicted `VERIFY_RECORD_REDACTED`
  - state: expected `PRESENT`; predicted `REDACTED`
- Step 12 mismatch:
  - system_id: expected `support_platform`; predicted `analytics_platform`
  - resource_id: expected `support_6477`; predicted `analytics_3697`
  - operation: expected `VERIFY_RECORD_REDACTED`; predicted `VERIFY_RECORD_ANONYMIZED`
  - state: expected `REDACTED`; predicted `ANONYMIZED`
- Step 13 mismatch:
  - system_id: expected `analytics_platform`; predicted `integration_service`
  - resource_id: expected `analytics_3697`; predicted `data_flow_8524`
  - operation: expected `VERIFY_RECORD_ANONYMIZED`; predicted `VERIFY_DATA_FLOW_DISABLED`
  - state: expected `ANONYMIZED`; predicted `DISABLED`
- Missing predicted step 14: `{"step_no": 14, "phase": "VERIFICATION", "system_id": "integration_service", "resource_id": "data_flow_8524", "operation": "VERIFY_DATA_FLOW_DISABLED", "state": "DISABLED", "evidence_id": ""}`

## case_31
- Expected status: `COMPLETE`
- Predicted status: `COMPLETE`
- Expected steps: 3; predicted steps: 3
- Step 1 mismatch:
  - resource_id: expected `account_4857`; predicted `account_541`
  - evidence_id: expected `evidence_51`; predicted `evidence_90`

## case_32
- Expected status: `INCOMPLETE`
- Predicted status: `INCOMPLETE`
- Expected steps: 5; predicted steps: 5
- Step 3 mismatch:
  - resource_id: expected `account_8858`; predicted `account_542`
