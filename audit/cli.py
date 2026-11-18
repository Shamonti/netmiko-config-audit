import argparse
import sys

from audit.collector import load_configs
from audit.report import print_summary, write_csv
from audit.rules import evaluate, load_rules


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m audit",
        description="Audit network device configs against YAML rules.",
    )
    p.add_argument("--inventory", help="device inventory YAML (live mode, v0.2)")
    p.add_argument("--rules", default="rules/baseline.yaml", help="rules YAML file")
    p.add_argument("--output", default="reports/audit.csv", help="CSV report path")
    p.add_argument("--configs", help="folder of config files (offline mode)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.configs:
        print(
            "error: live mode (SSH) is not in v0.1; use --configs <folder>",
            file=sys.stderr,
        )
        return 2
    rules = load_rules(args.rules)
    rows = [
        row
        for d in load_configs(args.configs)
        for row in evaluate(d["device"], d["vendor"], d["config"], rules)
    ]
    write_csv(rows, args.output)
    print_summary(rows)
    return 1 if any(r["status"] == "FAIL" for r in rows) else 0
