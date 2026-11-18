import csv
from pathlib import Path

from audit.cli import main

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = str(ROOT / "samples")
BASELINE = str(ROOT / "rules" / "baseline.yaml")


def test_samples_fail_exit_1_and_csv_written(tmp_path):
    out = tmp_path / "sub" / "audit.csv"
    argv = ["--configs", SAMPLES, "--rules", BASELINE, "--output", str(out)]
    assert main(argv) == 1
    rows = list(csv.DictReader(out.open(encoding="utf-8")))
    assert rows and set(rows[0]) == {"device", "rule_id", "status"}
    assert {r["status"] for r in rows} == {"PASS", "FAIL"}


def test_all_pass_exit_0(tmp_path):
    cfgs = tmp_path / "cfgs"
    cfgs.mkdir()
    (cfgs / "cisco_ios_r1.cfg").write_text("hostname r1\n", encoding="utf-8")
    rules = tmp_path / "rules.yaml"
    rules.write_text(
        "rules:\n"
        "  - {id: T-1, vendor: cisco_ios, type: must_contain, value: hostname}\n",
        encoding="utf-8",
    )
    out = tmp_path / "out.csv"
    argv = ["--configs", str(cfgs), "--rules", str(rules), "--output", str(out)]
    assert main(argv) == 0
    assert "T-1,PASS" in out.read_text(encoding="utf-8")


def test_no_configs_exit_2(capsys):
    assert main([]) == 2
    assert "not in v0.1" in capsys.readouterr().err
