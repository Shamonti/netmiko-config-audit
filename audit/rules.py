import re
from dataclasses import dataclass
from pathlib import Path

import yaml

TYPES = ("must_contain", "must_not_contain", "must_match", "must_not_match")


@dataclass(frozen=True)
class Rule:
    id: str
    vendor: str
    type: str
    value: str


def load_rules(path: str | Path) -> list[Rule]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    rules = [Rule(r["id"], r["vendor"], r["type"], r["value"]) for r in data["rules"]]
    for r in rules:
        if r.type not in TYPES:
            raise ValueError(f"rule {r.id}: unknown type '{r.type}'")
    return rules


def check(rule: Rule, config: str) -> bool:
    if rule.type == "must_contain":
        return rule.value in config
    if rule.type == "must_not_contain":
        return rule.value not in config
    found = re.search(rule.value, config, re.MULTILINE) is not None
    return found if rule.type == "must_match" else not found


def evaluate(device: str, vendor: str, config: str, rules: list[Rule]) -> list[dict[str, str]]:
    return [
        {"device": device, "rule_id": r.id, "status": "PASS" if check(r, config) else "FAIL"}
        for r in rules
        if r.vendor == vendor
    ]
