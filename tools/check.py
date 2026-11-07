#!/usr/bin/env python3
"""Checks for the built site, run in CI.

- generated data is valid and every driver has a status
- no broken internal links
- no page over budget (home under 100 KB)
- the site never names a bug in libsigrok
"""

import json
import os
import re
import sys
import glob
import hashlib

failures = []

# 1. generated data is valid; every driver has a status
data_path = "data/drivers.json"
if not os.path.isfile(data_path):
    failures.append(f"missing {data_path}")
else:
    data = json.loads(open(data_path).read())
    drivers = data["drivers"]
    if not drivers:
        failures.append("no drivers in the data")
    for d in drivers:
        if not d.get("status"):
            failures.append(f"driver {d['key']} has no status")
    m = data["meta"]
    for k in ("version", "ported", "libsigrok_total", "cases_total", "hardware"):
        if k not in m:
            failures.append(f"meta missing {k}")
    print(f"data: {len(drivers)} drivers, {m.get('ported')} ported of "
          f"{m.get('libsigrok_total')}, {m.get('cases_total')} cases")

# 2. no broken internal links
broken = 0
for f in glob.glob("public/**/*.html", recursive=True):
    html = open(f, encoding="utf-8", errors="ignore").read()
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http", "#", "mailto")):
            continue
        path = href.split("#")[0].split("?")[0]
        if not path:
            continue
        base = os.path.dirname(f)
        target = ("public" + path) if path.startswith("/") else \
            os.path.normpath(os.path.join(base, path))
        if not os.path.exists(target):
            broken += 1
            failures.append(f"broken link in {f}: {href}")
print(f"links: {broken} broken")

# 3. no page over budget
over = 0
for f in glob.glob("public/**/*.html", recursive=True):
    size = os.path.getsize(f)
    budget = 100 * 1024
    if size > budget:
        over += 1
        failures.append(f"page over budget ({size} > {budget}): {f}")
print(f"budget: {over} pages over 100 KB")

# 4. the site never names a bug in libsigrok
for f in glob.glob("public/**/*.html", recursive=True):
    text = open(f, encoding="utf-8", errors="ignore").read().lower()
    for m in re.finditer(r"libsigrok", text):
        window = text[max(0, m.start() - 40):m.end() + 40]
        if "bug" in window:
            failures.append(f"libsigrok near 'bug' in {f}")
            break

# 5. the UI screenshots match the manifest (present, unbroken, no strays)
ui_path = "data/ui.json"
if os.path.isfile(ui_path):
    ui = json.loads(open(ui_path).read())["ui"]
    for name, meta in ui["files"].items():
        p = os.path.join("public", "ui", name)
        if not os.path.isfile(p):
            failures.append(f"missing UI screenshot in public/ui: {name}")
            continue
        digest = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if digest != meta["sha256"] or os.path.getsize(p) != meta["size"]:
            failures.append(f"UI screenshot differs from manifest: {name}")
    # Only screenshots are tracked; public/ui/ also holds the page's own
    # index.html, which is not a stray.
    if os.path.isdir(os.path.join("public", "ui")):
        for name in os.listdir(os.path.join("public", "ui")):
            if name.endswith(".png") and name not in ui["files"]:
                failures.append(f"stray screenshot in public/ui: {name}")
    print(f"ui: {len(ui['files'])} screenshots (oxrok-ui {ui.get('version')})")
else:
    print("ui: manifest missing, skipped (run make ui)")

if failures:
    print("\nFAILURES:", file=sys.stderr)
    for f in failures:
        print(f"  {f}", file=sys.stderr)
    sys.exit(1)
print("all checks passed")
