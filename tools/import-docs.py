#!/usr/bin/env python3
"""Copy the reference docs that are safe to render into content/docs/.

The repo stays the source: this regenerates the copies on every build.
CLI.md, DEVICES.md, DRIVER_PORTING.md and ROADMAP.md name libsigrok's
bugs throughout, so they are not rendered; the CLI and USB guides are
written for the site, and USB.md goes too deep for a user guide.
DECODERS.md is copied, with front matter added, and with the phrase
"a libsigrok bug" neutralised so the site never names a bug in
libsigrok.
"""

import re
import sys
from pathlib import Path

repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "oxrok"
out = Path("content/docs")
out.mkdir(parents=True, exist_ok=True)

docs = {
    "DECODERS.md": ("decoders", "Protocol decoders"),
}

for src, (slug, title) in docs.items():
    text = (repo / "docs" / src).read_text()
    # The site does not name bugs in libsigrok; it says what oxrok does
    # and how it was checked.
    text = text.replace("a libsigrok bug", "a bug in the reference implementation")
    # Drop the H1; the front matter title takes its place.
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    body = "\n".join(lines).lstrip("\n")
    (out / f"{slug}.md").write_text(
        f"---\ntitle: {title}\n---\n\n{body}\n"
    )
    print(f"imported {src} -> content/docs/{slug}.md")
