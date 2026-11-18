from pathlib import Path

VENDORS = ("cisco_ios", "huawei_vrp")


def vendor_from_name(name: str) -> str:
    for v in VENDORS:
        if name.startswith(v + "_"):
            return v
    raise ValueError(f"cannot infer vendor from '{name}' (expected prefix one of {VENDORS})")


def load_configs(folder: str | Path) -> list[dict[str, str]]:
    """Return [{device, vendor, config}] for every file in folder."""
    return [
        {"device": p.stem, "vendor": vendor_from_name(p.stem), "config": p.read_text(encoding="utf-8")}
        for p in sorted(Path(folder).iterdir())
        if p.is_file()
    ]
