import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = ROOT / "dataset" / "sample_output.csv"
PREDICTED = ROOT / "output.csv"
REPORT = ROOT / "code" / "evaluation" / "step_mismatch_report.md"

FIELDS = [
    "step_no", "phase", "system_id", "resource_id",
    "operation", "state", "evidence_id"
]

def load_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = {}
        for row in csv.DictReader(f):
            case_id = row["case_id"]
            steps = json.loads(row.get("steps_json") or "[]")
            rows[case_id] = {
                "status": row.get("deletion_status", ""),
                "steps": steps
            }
        return rows

def main():
    expected = load_csv(EXPECTED)
    predicted = load_csv(PREDICTED)

    lines = [
        "# Sample Output Diagnostic Report",
        "",
        f"- Expected cases: {len(expected)}",
        f"- Predicted cases: {len(predicted)}",
        ""
    ]

    common = sorted(set(expected) & set(predicted))
    status_correct = 0
    exact_correct = 0
    position_correct = 0
    position_total = 0
    field_correct = 0
    field_total = 0

    for case_id in common:
        exp = expected[case_id]
        got = predicted[case_id]

        if exp["status"] == got["status"]:
            status_correct += 1

        if exp["steps"] == got["steps"]:
            exact_correct += 1

        lines.append(f"## {case_id}")
        lines.append(f"- Expected status: `{exp['status']}`")
        lines.append(f"- Predicted status: `{got['status']}`")

        if exp["status"] != got["status"]:
            lines.append("- **STATUS MISMATCH**")

        e_steps = exp["steps"]
        p_steps = got["steps"]
        max_len = max(len(e_steps), len(p_steps))

        if e_steps != p_steps:
            lines.append(f"- Expected steps: {len(e_steps)}; predicted steps: {len(p_steps)}")

        for i in range(max_len):
            e = e_steps[i] if i < len(e_steps) else None
            p = p_steps[i] if i < len(p_steps) else None

            if e is not None and p is not None:
                position_total += 1
                if e == p:
                    position_correct += 1

                for field in FIELDS:
                    field_total += 1
                    if e.get(field) == p.get(field):
                        field_correct += 1

                differences = [
                    f"{field}: expected `{e.get(field)}`; predicted `{p.get(field)}`"
                    for field in FIELDS
                    if e.get(field) != p.get(field)
                ]
                if differences:
                    lines.append(f"- Step {i + 1} mismatch:")
                    lines.extend(f"  - {d}" for d in differences)

            elif e is not None:
                lines.append(f"- Missing predicted step {i + 1}: `{json.dumps(e, ensure_ascii=False)}`")
            else:
                lines.append(f"- Extra predicted step {i + 1}: `{json.dumps(p, ensure_ascii=False)}`")

        if e_steps == p_steps:
            lines.append("- Step sequence: exact match")

        lines.append("")

    total = len(common)
    lines[4:4] = [
        "## Metrics",
        f"- Status accuracy: {status_correct}/{total} = {status_correct / total:.2%}" if total else "- Status accuracy: N/A",
        f"- Exact sequence accuracy: {exact_correct}/{total} = {exact_correct / total:.2%}" if total else "- Exact sequence accuracy: N/A",
        f"- Step-position accuracy: {position_correct}/{position_total} = {position_correct / position_total:.2%}" if position_total else "- Step-position accuracy: N/A",
        f"- Field accuracy: {field_correct}/{field_total} = {field_correct / field_total:.2%}" if field_total else "- Field accuracy: N/A",
        f"- Missing predicted cases: {len(set(expected) - set(predicted))}",
        f"- Unexpected predicted cases: {len(set(predicted) - set(expected))}",
        ""
    ]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Diagnostic report created: {REPORT}")
    print(f"Cases compared: {total}")
    print(f"Status accuracy: {status_correct}/{total}")
    print(f"Exact sequence accuracy: {exact_correct}/{total}")

if __name__ == "__main__":
    main()
