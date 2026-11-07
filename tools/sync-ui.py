#!/usr/bin/env python3
"""Synchronise the oxrok-ui screenshots into the site.

The UI's screenshots live in the oxrok-ui repo, docs/screenshots/, and are
regenerated on every release (cargo test --test screenshots -- --ignored).
This copies them into static/ui/ and writes data/ui.json, a manifest that
records which release they came from and a hash of each, so the build check
can tell a good copy from a stale or broken one.

The source is the sibling ../ui checkout, or a path passed as the first
argument. Run it after a UI release (make ui) and commit static/ui/ and
data/ui.json; the build runs it too, so the deployed site carries the
release's screenshots. When the source checkout is absent (e.g. in CI, where
the screenshots are committed) it refreshes the manifest from the committed
static/ui/ instead, preserving the recorded version.
"""

import hashlib
import json
import sys
from pathlib import Path


def ui_version(root: Path) -> str:
    toml = root / "Cargo.toml"
    if toml.is_file():
        for line in toml.read_text().splitlines():
            if line.startswith("version = "):
                return line.split("=", 1)[1].strip().strip('"')
    return "unknown"


def manifest_from_files(out: Path, source: str, version: str) -> dict:
    files = {}
    for p in sorted(out.glob("*.png")):
        data = p.read_bytes()
        files[p.name] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
    return {"ui": {"version": version, "source": source, "files": files}}


def write_manifest(manifest: dict) -> None:
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("data/ui.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../ui")
    src = root / "docs" / "screenshots"
    out = Path("static/ui")

    if src.is_dir():
        names = sorted(p.name for p in src.glob("*.png"))
        if not names:
            sys.exit(f"no screenshots in {src}")
        out.mkdir(parents=True, exist_ok=True)
        # Drop any the source no longer has, so a removed shot does not linger.
        for p in out.glob("*.png"):
            if p.name not in names:
                p.unlink()
        for name in names:
            (out / name).write_bytes((src / name).read_bytes())
        write_manifest(manifest_from_files(out, str(src), ui_version(root)))
        print(f"synced {len(names)} screenshots from {src} (oxrok-ui {ui_version(root)})")
        return

    # No source checkout (e.g. CI): the screenshots are committed, so just
    # refresh the manifest from them so the check can verify integrity.
    if out.is_dir() and any(out.glob("*.png")):
        version = "unknown"
        mp = Path("data/ui.json")
        if mp.is_file():
            try:
                version = json.loads(mp.read_text())["ui"].get("version", "unknown")
            except Exception:
                pass
        write_manifest(manifest_from_files(out, "committed", version))
        print(f"no {src}; manifest refreshed from committed {out}")
        return

    sys.exit(f"no screenshots in {src} and none committed in {out}")


if __name__ == "__main__":
    main()
