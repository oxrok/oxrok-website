#!/usr/bin/env python3
"""Generate the per-decoder page stubs from data/decoders.json.

As with the driver stubs (tools/gen-driver-pages.py), each stub carries
only the decoder's id; the template renders everything from the data.
Decoder ids and names are not translated (they are what a user types
after -P), so the stub is the same in every language.

Keep LANGUAGES in sync with the [languages.*] blocks in hugo.toml.
"""

import json
from pathlib import Path

LANGUAGES = ["en", "zh", "es"]

data = json.loads(Path("data/decoders.json").read_text())

for lang in LANGUAGES:
    out = Path("content/decoders") if lang == "en" else Path("content") / lang / "decoders"
    out.mkdir(parents=True, exist_ok=True)

    # Remove old stubs so a removed decoder does not leave a page behind,
    # but keep the section's _index.md (its title is localized per language).
    for f in out.glob("*.md"):
        if f.name == "_index.md":
            continue
        f.unlink()

    for d in data["decoders"]:
        title = json.dumps(d["name"], ensure_ascii=False)
        (out / f"{d['id']}.md").write_text(
            f"---\nkey: {d['id']}\ntitle: {title}\ntype: decoders\n---\n"
        )

    print(f"generated {len(data['decoders'])} decoder page stubs for {lang}")
