# oxrok.dev: website plan

A static site for oxrok, built with Hugo and hosted on GitHub Pages at
`oxrok.dev`. This is a plan to react to. Nothing is built yet. Decisions marked
**(open)** are collected at the end.

## What the site is for

A person arrives with a logic analyzer, a scope or a meter on the desk, or a
sigrok setup they know. In under a minute they should be able to answer:

1. What is oxrok?
2. Does it work with my device, and how far can I trust that?
3. How do I install it and capture something?

Everything else serves those three. Second audience: people curious how an
AI-assisted port can be tested without the hardware, which is where the emulator
story and `vusb` come in.

## Principles

- **Lean.** Few pages, short pages. Cut anything a user wouldn't miss.
- **Direct.** A command beats a paragraph. First screen shows a real command and
  real output.
- **Honest.** Most drivers have never met their device, and the site says so
  plainly, on every driver. That honesty is the selling point: nobody else tells
  you exactly how a driver was checked.
- **About oxrok, not about libsigrok's bugs.** The site doesn't mention bugs in
  libsigrok, here or on any page. It says what oxrok does and how it was checked.
- **Generated, not written.** Driver facts come from the repo at build time, so
  they can't go stale or be overclaimed by hand.
- **Beautiful through restraint.** One typeface family and a monospace, the logo's
  colours, generous space, no stock images, no animation for its own sake.
- **Fast and small.** No framework, no tracking, no cookie banner. Works without
  JavaScript, except search. Light and dark from the system setting.

## Hugo setup

- **Hugo extended**, pinned in CI. Not installed on this box yet; Fedora has
  0.162.1.
- **Own minimal layouts, no theme.** I earlier suggested Hextra, but a theme brings
  its look and its weight, and the bar here is lean and beautiful. A few templates
  and one small CSS file are easy to get right, and easy to keep. If that proves
  slow, fall back to Hextra for the docs pages only.
- **Pagefind** for search, run after the build over the HTML. It's a single binary,
  and search loads only when used.
- **Plain CSS**, no Tailwind or Node step. Hugo's own pipeline can fingerprint it.
- **Rust API docs** stay on docs.rs, linked from the nav.

## Site map

```
/                 Home
/install/         Install
/start/           Getting started
/devices/         All drivers: table with status and filters
/devices/<id>/    One page per driver
/testing/         How oxrok is tested
/vusb/            vusb, the virtual USB library
/docs/...         Reference, from the repo's docs
/blog/            Posts, with RSS
```

Top nav: **Devices · Get started · Testing · Docs · Blog**, plus GitHub. Keep it
to five.

## The pages

### Home

1. The oxrok logo, and one sentence: a sigrok-compatible stack in Rust for logic
   analyzers, scopes and meters, built with `cargo` alone. Then "Experimental. Most
   drivers have never run on real hardware", visible, not in small print.
2. A terminal block with one real capture, so it's obvious what it does:
   ```
   $ cargo install oxrok --version 0.1.0-alpha.2 --locked
   $ oxrok -d demo --samples 8 -O bits
   ```
   Output taken from a real run at build time, not typed by hand.
3. Three short columns: **Same interface as sigrok** (flags, formats, driver and
   decoder ids; Python decoders run unchanged) · **One binary** (no C libraries,
   static builds for Linux, macOS, Windows) · **Tested against the C**.
4. A status strip, generated: "68 of libsigrok's 87 drivers, 7,700 emulator cases,
   N on real hardware", linking to Devices.
5. A device search box leading into the table, as that's the first question.
6. A short teaser for the emulator and vusb, with vusb's logo.

The "written by an LLM, directed by a person" fact must be on the home page, in
words as plain as the README's. Honest and brief, not a boast or an apology.

### Install

One page: `cargo install`, release archives per platform with checksums, Linux
udev rules, macOS and Windows notes, features (`rustpython`, `python`, `libusb`),
and firmware: where to get what a device needs. From README "Installing" and
"Features".

### Getting started

A path of five small steps, each a command and its output, using `demo` so anyone
can follow with no hardware:

1. List drivers: `oxrok -L`.
2. Scan and show: `oxrok -d demo --show`.
3. Capture: samples, time, channels, output formats.
4. Trigger: `-t D0=r`, then `-w`. This was a real stumble: `D0:r` is wrong, and a
   command with no limit only prints usage. Show the right form, and call that out.
5. Decode: `-P uart:rx=D0`, then `-A`.

Then real devices: `conn=`, permissions, a serial example, a SCPI example. A short
**Coming from sigrok-cli** section: what's the same, and the differences that bite
(a failed capture exits 1, stricter values). It links to `docs/CLI.md`.

### Devices: the table

The heart of the site. A single table of drivers, generated, working with no
JavaScript, with a small script adding filter and search.

Columns: **Device / driver id · Kind · Connection · Status · Cases · Coverage**

**Status** is the key idea, with one clear word and colour, defined at the top:

| Status | Meaning |
|---|---|
| **Hardware** | Run on the real device, by us |
| **Stand-in** | Run over a real bus on a microcontroller acting as the device |
| **Emulated** | Compared with libsigrok on an emulated device; never on hardware |
| **Replay** | Checked only against recordings |
| **Not ported** | In libsigrok, not here yet, with the reason if known (GPIB, BLE) |

Colour must never be the only signal. A driver can hold more than one, so the table
shows the strongest, and the page shows them all. "How far can I trust this?" gets
a one-line answer at the top, linking to `/testing/`.

Filters: by kind (logic analyzer, scope, meter, supply, load, generator, other), by
status, by connection (USB, serial, TCP, HID). Text search over names, including
the many meter models behind `serial-dmm`: searching "UT61E" must find its driver.

Also a **"Have one? Tell us"** link: reports from real units are what the project
most lacks. It goes to a GitHub issue template with the command to run and what to
paste. Worth more than any other call to action on the site.

### Devices: one page per driver

Generated from one template, short:

- Name, status badge, vendor and models covered.
- **Connect:** the exact `-d` line, serial settings, ids, firmware needed.
- **Capabilities:** channels, sample rates, options with their ranges, get or set.
  From `--show` goldens where they exist.
- **Try it:** two or three commands.
- **How it was checked:** hardware or stand-in used, cases by class, coverage, what
  the model doesn't cover.
- **Behaviour to know:** what oxrok does, in oxrok's terms: "a capture fails with
  exit 1 after 10 s with no sample", "`-C` is honoured".
- **Known limits:** of oxrok and of the device's format. Often the most useful part:
  "a set may not have reached a live supply", "bit flips can't be detected",
  "temperatures below zero read as nothing".
- Links: source, model, scenario, `docs/DEVICES.md` section, report a result.

These come from `docs/drivers.toml`, written for the site, and not lifted from
`docs/DEVICES.md` or `docs/CLI.md`, which name C's bugs throughout. No line says what
libsigrok gets wrong. Where oxrok differs from sigrok-cli a user needs to know the
behaviour, and it can be stated with no judgement of the C.

### Testing

The most interesting page for developers, and it needs a diagram. Short, in this
order:

1. **The problem:** 87 drivers and almost none of the hardware.
2. **The idea, in one picture:** a device model in Rust, attached through Linux's
   `vhci-hcd` over USB/IP, so the kernel sees real hardware. The real `sigrok-cli`
   and `oxrok` run unmodified against the same device, and every transaction is
   logged. Then compare.
3. **What's compared:** output, errors, exit status, every USB transfer, plus gcov
   on the C driver to see what was reached.
4. **Models are hostile:** stalls, unplugs, late replies, bad frames.
5. **What it can't tell you:** the model and port share the writer's reading of a
   document; a model answers too fast. So real evidence outranks it: recordings,
   manuals, history. This limit stated frankly is what makes the page credible.
6. **Reviews:** builder, adversarial reviewer, mutation testing, stalls. Examples
   here are bugs found in oxrok's own ports, such as a late reply shifting every
   later reading, which are good stories and need no mention of the C.

Numbers generated. Links to `README` "How drivers are tested" and `docs/USB.md`.

### vusb

A page, not a section: `vusb` is its own project, and useful beyond oxrok. Its logo,
one sentence ("puts a USB device on the bus that is only Rust code"), a short model
example, what it offers (class shells, fault injection, the transaction log), and
that oxrok's whole test approach rests on it. Links to its repo, crates.io and
docs.rs. Its own site later, if it earns one **(open)**.

### Docs

Reference, rendered with a sidebar: a user's guide to the CLI (`oxrok` options,
outputs, triggers, decoders), and `DECODERS` and `USB`. A build step copies what it
can and adds front matter, so the repo stays the source.

`docs/CLI.md`, `DEVICES.md`, `DRIVER_PORTING.md` and `ROADMAP.md` name libsigrok's
bugs throughout, so **they are not rendered on the site**. They stay in the repo, for
developers, with at most a plain link from the footer. So the CLI guide is written
for the site, from `oxrok --help` and the parts of `CLI.md` about oxrok itself. Check
each imported file for such mentions, and have CI grep the built site for
`libsigrok` near "bug".

### Blog

Simple list, RSS. First post from `~/oxrok-blogpost.md` once it's written and the
questions at its end are settled.

## Data: where driver facts come from

Generate `data/drivers.json` at build time from a checkout of oxrok, with a small
script in the oxrok repo (`tools/site-data`, so it changes with what it reads).
Never edited by hand.

| Fact | Source |
|---|---|
| Driver ids and names | `oxrok -L` |
| Cases, by class | `tests/emu/MODEL/*.out` and `tools/emu/MODEL.sh` |
| Coverage | `tests/emu/MODEL/gcov.txt` |
| Hardware, stand-in | README's "What has been checked how". **This needs a structured source: see below.** |
| Capabilities | `tests/emu/MODEL/show*.out` where present; else from the driver's options |
| Behaviour, limits | `docs/drivers.toml`, written for the site |
| Not ported | libsigrok's driver list against `src/lib.rs` |
| Models behind a family | the driver's table (`serial-dmm` has 69 meters) |

**Work needed in the oxrok repo, which is its own small task:**
- A structured `docs/drivers.toml`: per driver, kind, connection, vendor and models,
  hardware evidence (what unit, what was run, when), and a few plain lines of
  behaviour and limits. The README's tables could then be generated from it too, so
  there's only one source. This is the file a person maintains, and where a user's
  report ends up. A first draft of its text can be drawn from `docs/DEVICES.md`,
  dropping what's about the C.
- The site build fails if a driver has no entry, so a new port can't appear without
  its status.

## Look and feel

- **Logo:** `docs/logo/lockup.svg` for the header, `mark.svg` for the favicon,
  `mono.svg` for places colour doesn't suit, `avatar.png` for social cards. vusb's
  from `~/vusb/docs/logo`. Palette taken from the logo; nothing competes with it.
  Check both logos on a dark background, as they may need `mono.svg` there.
- **Type:** system font stack for text, system monospace for commands. No web fonts:
  fast, and looks native. Comfortable line length of about 70 characters.
- **Layout:** a single centred column; only the devices table goes wider.
- **Terminal blocks:** the signature element. Real output, a copy button, no fake
  window chrome.
- **Status badges:** the one place with several colours, each with a word.
- **Diagram:** one inline SVG on Testing, in the logo's colours, working in dark
  mode. vusb's README has one to draw on.
- **Mobile:** fine at phone width. On a phone the table folds into rows, keeping
  device and status.
- **Budget:** home page under 100 KB with no images but the logo. Lighthouse 100s
  are a by-product, not a goal.

## Repository and hosting

- **Repo:** `oxrok/website`, checked out at `~/website`. A separate repo keeps site
  churn out of the code's history. Its build checks out `oxrok/oxrok` at a released
  tag for data, and rebuilds on a schedule and on release.
- **Which oxrok the site describes:** the driver table should say what's installable,
  so the latest release, with `main` flagged as "in development". A ported driver
  not yet released shows that **(open)**.
- **GitHub Pages:** an Actions workflow builds and deploys, with `CNAME` for
  `oxrok.dev`. DNS is on your side. `.dev` requires HTTPS, which Pages provides after
  the domain is verified.
- **Checks in CI:** broken link check, generated data valid, every driver has a
  status, no page over budget.

## Build order

1. **Skeleton:** Hugo, base template, CSS, logo, light and dark, Home with real
   content. Review how it looks before going further: it's where lean and beautiful
   is won or lost.
2. **Data:** `docs/drivers.toml` and `tools/site-data` in the oxrok repo; the devices
   table.
3. **Driver pages** from the template.
4. **Install, Getting started, Testing, vusb.** Words written by hand, kept short.
5. **Docs import, search, blog.**
6. **Publish:** workflow, domain, issue template for hardware reports.

Each step is reviewable locally with `hugo server` before anything is public. Steps
1 and 2 are the ones worth your eye.

## Not doing

Versioned docs (alpha; `main` and latest are enough), translations, a comments
system, analytics (**open**), a logo redesign, per-model pages for all 69 meters
(they're rows on `serial-dmm`'s page, findable by search), API docs beyond a link to
docs.rs, and a Fluke-style marketing tone.

## Decided

- **Repo:** `oxrok/website`.
- **libsigrok's bugs:** no mention anywhere on the site. The reference docs that name
  them stay in the repo and aren't rendered.

## Open questions

1. **Which state to show:** latest release (my suggestion), or `main`?
2. **Analytics:** none (my suggestion), or something privacy-respecting?
3. **How prominently to say "LLM-written":** I'd say plainly on the home page, as the
   README does.
4. **Hardware reports:** is a GitHub issue template the right door, and are you happy
   to be the one receiving them?
5. **vusb's page:** on oxrok.dev, or its own site later, with a domain?
6. **Name of the "Testing" page:** it could be "How we know", which is more honest
   about the question it answers.
