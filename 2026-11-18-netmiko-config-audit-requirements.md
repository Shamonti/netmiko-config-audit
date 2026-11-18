# netmiko-config-audit: Requirements (v0.1)

Portfolio project 1. A public, open-source tool that pulls network device configs over SSH, checks them against YAML rules, and reports pass/fail per device.

## 1. Goal
Show recruiters and clients one working, well-built tool that combines network automation (Netmiko) with DevOps practice (Docker, tests, CI).

## 2. Hard rules
- No company data: no real IPs, hostnames, configs, client names.
- All sample configs are synthetic and written from scratch.
- Credentials only from environment variables. Never in code, YAML, or git history.
- `.gitignore` covers `inventory/devices.yaml`, `.env`, `reports/`.

## 3. Users
- Network engineer who wants a quick compliance check across many devices.
- Reviewer (recruiter or client) who reads the README and runs the demo in under 5 minutes, without real devices.

## 4. Scope

### Must have (v0.1, MVP)
| ID | Requirement | Done when |
|---|---|---|
| R1 | CLI entry point `python -m audit` with `--help`, `--inventory`, `--rules`, `--output` | `python -m audit --help` prints usage |
| R2 | Offline mode: audit config files from a folder (`--configs samples/`) with no SSH | Demo runs with zero devices |
| R3 | YAML rules: `must_contain`, `must_not_contain`, `must_match` (regex), `must_not_match`, filtered by `vendor` | Each rule type has a passing and a failing test |
| R4 | Vendors: Cisco IOS/IOS-XE and Huawei VRP | Sample config and rules for each |
| R5 | Report: CSV plus a readable terminal summary (device, rule id, PASS/FAIL) | CSV written to `reports/` |
| R6 | Exit code 0 if all pass, 1 if any fail | Usable in CI pipelines |
| R7 | Unit tests with pytest against `samples/` only | `pytest` passes locally |
| R8 | Dockerfile, slim Python base, runs as non-root user | `docker run <image> --help` works, `whoami` is not root |
| R9 | README: what, why, quick start (local and Docker), example rule, example output | A stranger can run the demo from the README |

### Should have (v0.2)
| ID | Requirement |
|---|---|
| S1 | Live mode: pull running config over SSH with Netmiko (`show running-config` / `display current-configuration`) |
| S2 | Concurrent collection with `ThreadPoolExecutor`, configurable `--workers` |
| S3 | Per-device timeout and clear error rows for unreachable devices (audit continues) |
| S4 | HTML report |
| S5 | GitHub Actions: lint (ruff), tests, Docker build on every push |

### Could have (later)
- Diff against a golden config.
- Junos or Nokia support.
- Wrap the tool as an MCP server (ties to the Claude Academy MCP course).
- Lab demo against a free virtual lab (Containerlab or Cisco DevNet sandbox).

### Out of scope
- Pushing config changes to devices (read-only tool).
- Web UI or database.

## 5. Non-functional
- Python 3.11+, type hints, `ruff` clean.
- Logging with levels, no passwords in logs.
- Small dependency list: `netmiko`, `pyyaml`, `pytest` (dev).

## 6. Project layout
```
netmiko-config-audit/
├── audit/
│   ├── __init__.py
│   ├── __main__.py     # enables python -m audit
│   ├── cli.py
│   ├── collector.py    # SSH pull (v0.2) and file loader (v0.1)
│   ├── rules.py
│   └── report.py
├── inventory/devices.example.yaml
├── rules/baseline.yaml
├── samples/            # synthetic configs only
├── tests/test_rules.py
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

## 7. Milestones (about 1 hour a day)
| Milestone | Content | Proof |
|---|---|---|
| M1 Setup | Public repo, layout, `.gitignore`, `__main__.py`, Dockerfile (non-root) | `docker run` prints `--help` |
| M2 Rules engine | R3, R4, samples, tests | `pytest` green |
| M3 Reports | R5, R6, offline demo end to end | CSV in `reports/` |
| M4 README | R9, example output | Shareable repo link (v0.1 done) |
| M5 Live and CI | S1 to S5 | Green Actions badge (v0.2 done) |

## 8. Definition of done (v0.1)
All Must-have rows pass, repo is public, README demo works from a fresh clone, and no real data anywhere in the history.
