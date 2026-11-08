#!/usr/bin/env python3
"""Generate data/decoders.json from an oxrok checkout.

Usage: tools/decoder-data.py [oxrok-dir] > data/decoders.json

The facts come from the oxrok binary, never from this repo:

- `oxrok -L` lists the decoders the default build has. The default build
  has no Python host, so every decoder it lists is native.
- `oxrok -P <id> --show` gives each decoder's metadata (names, tags,
  inputs and outputs, channels, options, annotation classes and rows,
  binary classes, documentation), in sigrok-cli's format.
- docs/NATIVE_DECODERS.md gives the libsigrokdecode reference version,
  the decoder inventory, and per decoder the parity status and notes.

A libsigrokdecode decoder with no native version is listed as running
on the Python hosts only. A disagreement between the binary and the
checklist (a decoder marked native that the binary does not have, or the
other way round) fails the build.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1] if len(sys.argv) > 1 else "../oxrok").resolve()


def fail(msg):
    print(f"decoder-data: {msg}", file=sys.stderr)
    sys.exit(1)


binary = repo / "target" / "debug" / "oxrok"
if not binary.is_file():
    print("decoder-data: building oxrok", file=sys.stderr)
    subprocess.run(["cargo", "build"], cwd=repo, check=True)


def run(*args):
    return subprocess.run(
        [str(binary), *args], capture_output=True, text=True, check=True
    ).stdout


# 1. the decoders the default build has
native_ids = []
section = False
for line in run("-L").splitlines():
    if line.startswith("Supported protocol decoders:"):
        section = True
        continue
    if section and line.startswith("Supported"):
        break
    if section:
        m = re.match(r"\s+(\S+)\s+", line)
        if m:
            native_ids.append(m.group(1))
if not native_ids:
    fail("`oxrok -L` lists no protocol decoders")


# 2. per-decoder metadata from --show
SCALARS = {
    "ID": "id",
    "Name": "name",
    "Long name": "longname",
    "Description": "desc",
    "License": "license",
}
LISTS = {
    "Possible decoder input IDs": "inputs",
    "Possible decoder output IDs": "outputs",
    "Decoder tags": "tags",
    "Annotation classes": "annotations",
    "Annotation rows": "rows",
    "Binary classes": "binary",
    "Required channels": "channels",
    "Optional channels": "optional_channels",
    "Options": "options",
}


def parse_show(text):
    d = {v: [] for v in LISTS.values()}
    cur = None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line == "Documentation:":
            d["doc"] = "\n".join(lines[i + 1:]).strip()
            break
        key, sep, val = line.partition(": ")
        if sep and key in SCALARS:
            d[SCALARS[key]] = val
            cur = None
        elif line.endswith(":") and line[:-1] in LISTS:
            cur = LISTS[line[:-1]]
        elif line.startswith("- ") and cur:
            d[cur].append(line[2:])
        # "None." under a list header means the list is empty.
    d.setdefault("doc", "")

    def split(item):
        k, _, v = item.partition(": ")
        return k, v

    d["annotations"] = [dict(zip(("id", "desc"), split(a))) for a in d["annotations"]]
    d["binary"] = [dict(zip(("id", "desc"), split(b))) for b in d["binary"]]
    rows = []
    for r in d["rows"]:
        m = re.match(r"(\S+) \((.*?)\): ?(.*)", r)
        if m:
            rows.append({
                "id": m.group(1),
                "desc": m.group(2),
                "classes": [c for c in m.group(3).split(", ") if c],
            })
    d["rows"] = rows
    for k in ("channels", "optional_channels"):
        chans = []
        for c in d[k]:
            m = re.match(r"(\S+) \((.*?)\): ?(.*)", c)
            if m:
                chans.append({"id": m.group(1), "name": m.group(2), "desc": m.group(3)})
        d[k] = chans
    opts = []
    for o in d["options"]:
        name, desc = split(o)
        default, values = "", []
        m = re.search(r" \((.*)\)$", desc)
        if m:
            desc = desc[: m.start()]
            inner = m.group(1)
            dm = re.search(r"(?:^|, )default (.*)$", inner)
            if dm:
                default = dm.group(1).strip("'")
                inner = inner[: dm.start()]
            values = [v.strip().strip("'") for v in inner.split(", ") if v.strip()]
        opts.append({"id": name, "desc": desc, "default": default, "values": values})
    d["options"] = opts
    return d


decoders = {}
for did in native_ids:
    d = parse_show(run("-P", did, "--show"))
    if d.get("id") != did:
        fail(f"`oxrok -P {did} --show` reports id {d.get('id')!r}")
    decoders[did] = d


# 3. the checklist: reference version, inventory, status and notes
checklist = (repo / "docs" / "NATIVE_DECODERS.md").read_text()
m = re.search(r"Reference: libsigrokdecode ([\d.]+)", checklist)
if not m:
    fail("no 'Reference: libsigrokdecode X' line in docs/NATIVE_DECODERS.md")
reference = m.group(1)

rows = re.findall(
    r"^\| `([a-z0-9_]+)` \| (logic|stacked) \| [^|]+ \| ([^|]+) \| ([^|]+) \|$",
    checklist,
    re.M,
)
if not rows:
    fail("no checklist table in docs/NATIVE_DECODERS.md")

errors = []
upstream = {}
for did, kind, status, notes in rows:
    status, notes = status.strip(), notes.strip()
    upstream[did] = kind
    exception = ""
    if notes.startswith("exception:"):
        exception = notes[len("exception:"):].strip()
    native = status.startswith("native")
    if native and did not in decoders:
        errors.append(f"{did}: marked native in the checklist, not in `oxrok -L`")
    if did in decoders:
        decoders[did].update({
            "kind": kind,
            "parity": "parity-tested" in status,
            "exception": exception,
        })
    else:
        # In libsigrokdecode, not native: runs on the Python hosts only.
        decoders[did] = {
            "id": did, "name": did, "longname": "", "desc": "", "doc": "",
            "kind": kind, "parity": False, "exception": "",
            **{v: [] for v in LISTS.values()},
        }

for did in native_ids:
    if did not in upstream:
        errors.append(f"{did}: in `oxrok -L`, not in the checklist")

if errors:
    for e in errors:
        print(f"decoder-data: {e}", file=sys.stderr)
    sys.exit(1)


# 4. derived: status, stacking, an example command line
for d in decoders.values():
    d["native"] = d["id"] in native_ids
    if not d["native"]:
        d["status"] = "python"
    elif d["exception"]:
        d["status"] = "exception"
    elif d["parity"]:
        d["status"] = "parity"
    else:
        d["status"] = "native"
    d["input"] = d["inputs"][0] if d["inputs"] else ("logic" if d["kind"] == "logic" else "")


def provider(out_id):
    """The decoder that produces an output id: the one named after it first."""
    if out_id in decoders and out_id in decoders[out_id]["outputs"]:
        return decoders[out_id]
    for d in decoders.values():
        if out_id in d["outputs"]:
            return d
    return None


def spec(d):
    s = d["id"]
    # Required channels; with none (uart, parallel), the first optional one.
    for i, c in enumerate(d["channels"] or d["optional_channels"][:1]):
        s += f":{c['id']}=D{i}"
    return s


for d in decoders.values():
    chain, cur, seen = [d], d, {d["id"]}
    while cur["input"] and cur["input"] != "logic":
        p = provider(cur["input"])
        if not p or p["id"] in seen:
            break
        chain.insert(0, p)
        seen.add(p["id"])
        cur = p
    d["chain"] = [c["id"] for c in chain]
    d["example"] = "oxrok -i capture.sr -P " + ",".join(spec(c) for c in chain)
    d["stacked_by"] = sorted(
        o["id"] for o in decoders.values()
        if o["id"] != d["id"] and o["input"] and o["input"] in d["outputs"]
    )

# 5. examples: real runs on the captures in oxrok's tests/fixtures, so the
# output shown on the site is what this build prints. A command that fails,
# prints nothing, or names a decoder that does not exist fails the build.
# The page shows the capture by its file name. Titles and prose are the
# i18n keys dec_ex_<key>_h and dec_ex_<key>_p.
fixtures = repo / "tests" / "fixtures"
EXAMPLES = [
    ("uart", "uart-hi.vcd",
     ["-P", "uart:baudrate=115200:rx=top.D0:format=ascii", "-A", "uart=rx-data"], None),
    ("can", "decoders/can/mcp2515dm-bm-125kbits_msg_222_5bytes.sr",
     ["-P", "can:can_rx=CAN_RX:nominal_bitrate=125000", "-A", "can=fields"], None),
    ("midi", "decoders/midi/midi_key1.sr",
     ["-P", "uart:rx=RX:baudrate=31250,midi", "-A", "midi"], None),
    ("eeprom", "decoders/eeprom24xx/lcsoft-mini-board-fx2-init.sr",
     ["-P", "i2c:scl=SCL:sda=SDA,eeprom24xx", "-A", "i2c=addr-data,eeprom24xx=ops"], None),
    ("binary", "i2c-write-read.vcd",
     ["-P", "i2c:scl=top.scl:sda=top.sda", "-B", "i2c=data-write"], "xxd"),
    ("meta", "i2c-write-read.vcd",
     ["-P", "i2c:scl=top.scl:sda=top.sda", "-M", "i2c"], None),
]
MAX_LINES = 12


def xxd(data):
    lines = []
    for off in range(0, len(data), 16):
        chunk = data[off:off + 16]
        hexs = " ".join(chunk[i:i + 2].hex() for i in range(0, len(chunk), 2))
        text = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{off:08x}: {hexs:<39}  {text}")
    return "\n".join(lines)


examples = []
for key, capture, args, pipe in EXAMPLES:
    path = fixtures / capture
    if not path.is_file():
        errors.append(f"example {key}: missing capture {path}")
        continue
    pd = args[args.index("-P") + 1]
    for spec_ in pd.split(","):
        if spec_.split(":")[0] not in decoders:
            errors.append(f"example {key}: unknown decoder in {pd!r}")
    r = subprocess.run([str(binary), "-i", str(path), *args], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        errors.append(f"example {key}: exit {r.returncode}, {len(r.stdout)} bytes: "
                      f"{r.stderr.decode(errors='replace').strip()}")
        continue
    if pipe == "xxd":
        text = xxd(r.stdout)
    else:
        text = r.stdout.decode()
    lines = text.rstrip("\n").splitlines()
    more = len(lines) > MAX_LINES
    cmd = f"oxrok -i {Path(capture).name} {' '.join(args)}" + (" | xxd" if pipe == "xxd" else "")
    examples.append({
        "key": key,
        "cmd": cmd,
        "out": "\n".join(lines[:MAX_LINES]),
        "more": more,
        "chain": [s.split(":")[0] for s in pd.split(",")],
    })

if errors:
    for e in errors:
        print(f"decoder-data: {e}", file=sys.stderr)
    sys.exit(1)

out = sorted(decoders.values(), key=lambda d: d["id"])
tags = sorted({t for d in out for t in d["tags"]})
meta = {
    "reference": reference,
    "total": len(upstream),
    "native": sum(1 for d in out if d["native"] and d["id"] in upstream),
    "parity": sum(1 for d in out if d["parity"]),
    "exceptions": sum(1 for d in out if d["exception"]),
    "python_only": sum(1 for d in out if not d["native"]),
    "logic": sum(1 for d in out if d["kind"] == "logic"),
    "stacked": sum(1 for d in out if d["kind"] == "stacked"),
    "tags": tags,
}

json.dump({"meta": meta, "examples": examples, "decoders": out}, sys.stdout, indent=1, ensure_ascii=False)
print()
