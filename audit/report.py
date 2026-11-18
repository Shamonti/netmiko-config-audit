import csv
from pathlib import Path

FIELDS = ("device", "rule_id", "status")


def write_csv(rows: list[dict[str, str]], path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def print_summary(rows: list[dict[str, str]]) -> None:
    for r in rows:
        print(f"{r['device']:<24} {r['rule_id']:<12} {r['status']}")
    fails = sum(r["status"] == "FAIL" for r in rows)
    print(f"\n{len(rows) - fails} PASS, {fails} FAIL ({len(rows)} checks)")
