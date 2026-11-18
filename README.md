# netmiko-config-audit

Audits saved network device configs (Cisco IOS, Huawei VRP) against a YAML baseline and prints PASS/FAIL per rule.

**Why:** catch config drift and insecure settings (telnet, RW SNMP, missing logging) with a repeatable, scriptable check. The exit code makes it CI-friendly.

> Live SSH collection via Netmiko is planned for v0.2. v0.1 audits config files on disk.

## Quick start

Local:

```
pip install -r requirements.txt
python -m audit --configs samples/
```

Docker (bundles the samples as a demo):

```
docker build -t netmiko-config-audit .
docker run --rm netmiko-config-audit --configs samples/
```

Exit code is `0` if every check passes and `1` if any check FAILs.

## Example rule (`rules/baseline.yaml`)

```yaml
- {id: CISCO-002, vendor: cisco_ios, type: must_not_contain, value: "transport input telnet"}
- {id: CISCO-003, vendor: cisco_ios, type: must_match, value: '^logging host \d+\.\d+\.\d+\.\d+'}
```

Rule types: `must_contain`, `must_not_contain`, `must_match`, `must_not_match`.

## Example output

```
cisco_ios_edge1          CISCO-001    PASS
cisco_ios_edge1          CISCO-002    FAIL
cisco_ios_edge1          CISCO-003    PASS
cisco_ios_edge1          CISCO-004    FAIL
huawei_vrp_core1         HUAWEI-001   PASS
huawei_vrp_core1         HUAWEI-002   PASS
huawei_vrp_core1         HUAWEI-003   FAIL
huawei_vrp_core1         HUAWEI-004   PASS

5 PASS, 3 FAIL (8 checks)
```
