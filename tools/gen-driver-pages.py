#!/usr/bin/env python3
"""Generate the per-driver page stubs from data/drivers.json.

Each stub carries only the driver's key; the template renders everything
else from the data, so the pages can never drift from the facts. Stubs are
written for every configured language so each /<lang>/devices/ tree exists;
the stub is identical across languages because driver names are not
translated (they are what a user matches against `oxrok -L`).

Keep LANGUAGES in sync with the [languages.*] blocks in hugo.toml.
"""

import json
from pathlib import Path

LANGUAGES = ["en", "zh", "es"]

data = json.loads(Path("data/drivers.json").read_text())

for lang in LANGUAGES:
    out = Path("content/devices") if lang == "en" else Path("content") / lang / "devices"
    out.mkdir(parents=True, exist_ok=True)

    # Remove old stubs so a removed driver does not leave a page behind,
    # but keep the section's _index.md (its title is localized per language).
    for f in out.glob("*.md"):
        if f.name == "_index.md":
            continue
        f.unlink()

    for d in data["drivers"]:
        (out / f"{d['key']}.md").write_text(
            f"---\nkey: {d['key']}\ntitle: {d['name']}\ntype: devices\n---\n"
        )

    print(f"generated {len(data['drivers'])} driver page stubs for {lang}")
