# Cursor Agent Instructions

You are working on the HackerRank Orchestrate challenge "Ghost Data Still Exists".

Before editing:
1. Read the root `AGENTS.md` and `README.md`.
2. Read `problem_statement.md`.
3. Read `code/main.py` and the evidence/policy contract.
4. Use only participant-facing content under `dataset/`. Never inspect or use organizer-only files.
5. Never copy labels from `sample_output.csv` into prediction logic. It is allowed only for evaluation.

Engineering rules:
- Preserve the exact output contract: 518 sorted rows, columns `case_id,deletion_status,steps_json`.
- Use evidence available at or before `audit_at`; never treat `reported_status` or `system_activity.reported_result` as proof of final state.
- Resolve current and historical identifiers.
- Use `deletion_rules.csv` for all data categories and conditions.
- Retain security/legal records when policy says retain.
- Tombstones may keep stable `user_id`, but direct identifiers must be removed.
- Findings and COMPLETE verification steps need evidence IDs; proposed remediation and future verification use `""`.
- Step ordering: phase order first, then operation order from the contract, then system and resource ascending.
- Keep deterministic serialization and add regression tests for every fix.
- Do not invent evidence IDs, resources, states, or operations.
- Do not include secrets in code, logs, prompts, or the archive.

Run:
```bash
python code/main.py --evaluate-samples --json-report code/evaluation/sample_metrics.json
python code/main.py
python code/package_submission.py
```

When changing behavior, compare sample metrics before and after. Prefer evidence-grounded general rules over case IDs, fixture-specific shortcuts, or hardcoded labels.
