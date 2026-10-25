#!/usr/bin/env python3
"""Run the public sample comparison and contract tests."""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from main import compare_sample

if __name__ == "__main__":
    report = compare_sample(ROOT / "dataset")
    print(json.dumps({k: v for k, v in report.items() if k != "failures"}, indent=2))
    print(f"Exact-output mismatches: {len(report['failures'])}")
