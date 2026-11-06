#!/usr/bin/env python3
"""Generate the per-driver page stubs from data/drivers.json.

Each stub carries only the driver's key; the template renders everything
else from the data, so the pages can never drift from the facts.
"""

import json
from pathlib import Path

data = json.loads(Path("data/drivers.json").read_text())
out = Path("content/devices")
out.mkdir(parents=True, exist_ok=True)

# Remove old stubs so a removed driver does not leave a page behind.
for f in out.glob("*.md"):
    f.unlink()

for d in data["drivers"]:
    (out / f"{d['key']}.md").write_text(
        f"---\nkey: {d['key']}\ntitle: {d['name']}\n---\n"
    )

print(f"generated {len(data['drivers'])} driver page stubs")
