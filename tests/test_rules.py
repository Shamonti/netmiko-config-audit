from pathlib import Path

from audit.collector import load_configs
from audit.rules import evaluate, load_rules

ROOT = Path(__file__).resolve().parent.parent
RULES = load_rules(ROOT / "rules" / "baseline.yaml")
DEVICES = {d["device"]: d for d in load_configs(ROOT / "samples")}


def status(device: str, rule_id: str) -> str:
    d = DEVICES[device]
    res = evaluate(d["device"], d["vendor"], d["config"], RULES)
    return next(r["status"] for r in res if r["rule_id"] == rule_id)


def test_vendor_inferred_from_filename():
    assert DEVICES["cisco_ios_edge1"]["vendor"] == "cisco_ios"
    assert DEVICES["huawei_vrp_core1"]["vendor"] == "huawei_vrp"


def test_vendor_filter():
    d = DEVICES["huawei_vrp_core1"]
    res = evaluate(d["device"], d["vendor"], d["config"], RULES)
    ids = {r["rule_id"] for r in res}
    assert ids and all(i.startswith("HUAWEI") for i in ids)


def test_must_contain():
    assert status("cisco_ios_edge1", "CISCO-001") == "PASS"
    assert status("huawei_vrp_core1", "HUAWEI-001") == "PASS"


def test_must_contain_fails():
    from audit.rules import Rule, check

    cfg = DEVICES["cisco_ios_edge1"]["config"]
    assert not check(Rule("X", "cisco_ios", "must_contain", "no-such-line"), cfg)


def test_must_not_contain():
    assert status("huawei_vrp_core1", "HUAWEI-002") == "PASS"
    assert status("cisco_ios_edge1", "CISCO-002") == "FAIL"


def test_must_match():
    assert status("cisco_ios_edge1", "CISCO-003") == "PASS"
    assert status("huawei_vrp_core1", "HUAWEI-003") == "FAIL"


def test_must_match_fails():
    from audit.rules import Rule, check

    cfg = DEVICES["cisco_ios_edge1"]["config"]
    assert not check(Rule("X", "cisco_ios", "must_match", r"^ntp server \S+"), cfg)


def test_must_not_match():
    assert status("huawei_vrp_core1", "HUAWEI-004") == "PASS"
    assert status("cisco_ios_edge1", "CISCO-004") == "FAIL"
