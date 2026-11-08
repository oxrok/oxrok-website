# oxrok.dev internationalization plan

This is a plan, not work. It says how to make oxrok.dev available in several
languages without breaking the site's two hard rules: **facts never go stale**
and **generated, not written**. Decisions marked **(open)** are collected at the
end.

---

## 1. Goal and non-goals

**Goal.** A person who arrives at oxrok.dev with a logic analyzer, a scope or a
meter on the desk — and whose first language is not English — can answer the
same three questions the English site answers (what is oxrok, does it work with
my device, how do I install and capture something) in their own language.

**Non-goals.**

- No translation of the tool itself, its flags, driver ids, decoder ids, file
  formats, or program output. Those are identifiers and machine output; they
  stay as they are in every language. Translating them would break the "same
  interface as sigrok" promise and the "search UT61E finds its driver" promise.
- No translation of the blog for now (there is one index and no posts yet).
- No automatic language redirect (IP/geo sniffing). The site works without
  JavaScript except search, and we keep it that way. Language is chosen by the
  visitor, not guessed.
- No new web fonts. CJK and Cyrillic render from the system font stack, which is
  the point of that choice.

---

## 2. What there is to translate

The site is small, and much of it is machine output or data. The translatable
surface, in rough order of size:

| Layer | Where it lives today | Translatable prose (approx.) |
|---|---|---|
| UI chrome | `layouts/_default/baseof.html`, `index.html`, `devices/list.html`, `devices/single.html`, shortcodes, partials | ~200 short strings |
| Hand-written pages | `content/_index.md` (title only — prose is in `layouts/index.html`), `install.md`, `start.md`, `testing.md`, `vusb.md`, `ui.md`, `docs/_index.md`, `docs/cli.md`, `docs/usb.md` | ~3,100 words |
| Generated driver facts | `data/drivers.json` (from `../oxrok/tools/site-data` + `docs/drivers.toml`) | ~900 words today, across 38 drivers; grows as `drivers.toml` fills in |
| Reference docs | `content/docs/decoders.md` (imported from `../oxrok/docs/DECODERS.md` each build); `cli.md`/`usb.md` are hand-written | ~2,000 words, developer-facing |

The volumes are small enough that human translation is affordable; the main cost
is *keeping* them in sync, not producing them once.

---

## 3. Languages

**Ship first:** English (default), 简体中文 (`zh`), 日本語 (`ja`), Español
(`es`), Français (`fr`), Deutsch (`de`).

**Add next:** Русский (`ru`), 한국어 (`ko`).

**Defer:** Português, Italiano, हिन्दी, العربية.

Reasoning for the recommendations, briefly:

- **Russian** — a large, active electronics/sigrok-adjacent hobbyist and
  developer community with real hardware on desks and lower English comfort in
  its documentation culture than Western Europe. Second-tier, not first, only
  because it doubles the "second wave" of languages to review.
- **Korean** — a strong electronics-hobbyist and developer community, and CJK
  infrastructure (Pagefind tokenization, CSS line-height) is already paid for by
  Japanese and Chinese. Cheap to add after CJK works.
- **Portuguese** — a very large population, but the developer/tools audience
  reads English readily, and the marginal gain for a Rust CLI tool is modest.
  Defer; `pt-BR` first if it is ever added.
- **Italian** — small developer base with high English literacy; lowest
  value-per-word of the European languages. Defer.
- **Hindi** — enormous population, but technical and command-line documentation
  is overwhelmingly English-first; the audience that uses logic analyzers reads
  English. Near-zero near-term return. Defer.
- **Arabic** — requires right-to-left layout (`dir="rtl"`), mirrored UI, and
  RTL-aware CSS across every template, for a community where the target
  audience reads English. That engineering cost buys little today. Defer until
  RTL is worth it, or skip.

A note on Chinese variants: start with Simplified (`zh-Hans`). Traditional
(`zh-Hant`) is a separate translation job, not a flag; add it later if asked.

---

## 4. Architecture: URLs, default language, and Hugo setup

### 4.1 URL strategy: subpaths, not subdomains

Use **path-based** multilingual URLs, with English at the root:

```
/            English (unchanged)
/zh/         简体中文
/ja/         日本語
/es/         Español
/fr/         Français
/de/         Deutsch
/ru/ … /ko/  (later)
```

Reasons:

- **Existing URLs must not move.** English is already live at `/`, `/install/`,
  `/devices/`, and so on. Keeping English at the root preserves every existing
  link, RSS path, and search index with zero redirects.
- GitHub Pages on a custom domain serves one site from one repo. Subdomains
  (`zh.oxrok.dev`) would mean either multiple deployments or base-URL tricks,
  plus DNS records per subdomain and per-subdomain HTTPS. Subpaths are one build,
  one CNAME, one certificate.
- It is the Hugo default and the standard for open-source project sites.

The one thing subpaths give up is per-language subdomains for a future language
pick on a cookie/geo basis; we have already chosen no auto-redirect, so this
costs nothing.

### 4.2 Hugo configuration

`hugo.toml` gains a multilingual block. Sketch:

```toml
defaultContentLanguage = "en"
defaultContentLanguageInSubdir = false   # English stays at /

[languages.en]
languageCode = "en"
languageName = "English"
weight = 1

[languages.zh]
languageCode = "zh-Hans"
languageName = "简体中文"
weight = 2

[languages.ja]
languageCode = "ja"
languageName = "日本語"
weight = 3

# … es, fr, de (and later ru, ko)
```

Content layout follows Hugo's convention with the default language at the root:

```
content/                    # English (unchanged, no move)
content/zh/install.md       # translations
content/zh/devices/…        # per-driver stubs, see §6
content/ja/…
```

Because English stays in `content/`, the English tree is not touched at all —
this is the lowest-churn way in. The translation files are additive.

### 4.3 Language switcher

A compact selector in the header (right side, next to GitHub) and repeated in
the footer. Two options, both built from Hugo's per-page translation data:

- a `<select>` that navigates on change (small, no JS framework), or
- a short list of native-language links.

Keep it out of the five-item nav, which stays **Devices · Get started · Testing
· Docs · Blog**. The switcher shows native names (English, 简体中文, 日本語, …).

Hugo gives each page `.Translations` (its siblings in other languages) and
`.AllTranslations`. The switcher renders links from those, so a page with no
translation in a given language simply isn't offered a dead link for it — the
visitor falls back to English, which is correct behaviour during rollout.

### 4.4 SEO

- **`<html lang>` and `<title>`:** change `baseof.html` from hard-coded
  `lang="en"` to `lang="{{ .Site.Language.LanguageCode }}"`. Add
  `dir="rtl"` later if Arabic is ever added. Keep terminal blocks and code
  `dir="ltr"` regardless of page direction.
- **`hreflang`:** emit `<link rel="alternate" hreflang="…" href="…">` per page
  from `.AllTranslations`, plus `x-default` pointing at the English URL. Hugo
  has the data; the link is a few lines in `baseof.html`.
- **Sitemap:** Hugo generates one `sitemap.xml` covering all languages. The
  built-in template may not include `hreflang` alternates — override
  `layouts/sitemap.xml` to add them if we want cross-language discovery (worth
  doing, it is a small template). `robots.txt` is already generated
  (`enableRobotsTXT = true`); add a `Sitemap:` line pointing at `sitemap.xml`.
- **RSS:** with multiple languages Hugo emits per-language feeds. Update the
  RSS link in `baseof.html` to point at the current language's `index.xml`.

---

## 5. Translation by layer

### Layer 1 — UI chrome (nav, footer, buttons, labels)

**What it is:** the fixed words in templates: nav items, footer links, the
"copy"/"copied" button text, status names and their definitions, kind and
connection labels, column headers, filter labels and placeholders, "Covers",
"Connect", "Capabilities", "How it was checked", "Behaviour to know", "Known
limits", "Not ported yet.", "No driver id yet.", "all drivers →", "No drivers
match those filters.", the count line, and every `aria-label`.

**Approach:** move these into Hugo i18n catalogs — `i18n/en.toml`,
`i18n/zh.toml`, etc. — and reference them with `{{ i18n "key" }}` / `{{ T "key" }}`.
One string, one place, per language. A CI check diffs each catalog's keys
against `en.toml` so a new English string cannot appear without every language
being told about it.

**Feasibility:** fully feasible and cheap. This is the highest-value first step,
because it localizes the single most-read artifact on the site — the device
status table — without touching driver prose.

**Status vocabulary in detail:** status names (`Hardware`, `Stand-in`,
`Emulated`, `Software`, `Replay`, `Not ported`) and their one-line meanings are
exactly the "one clear word and colour" idea. Translate the words; **do not**
translate the machine values (`hardware`, `emulated`, …) that drive the CSS
classes and filters. The `dict` lookups in `devices/list.html` and
`devices/single.html` keep keying on the raw value and read the label from i18n.
Same for `kind` (`logic-analyzer`, `scope`, …) and `connection` (`usb`, `serial`,
…): display label from i18n, data value unchanged.

### Layer 2 — Hand-written pages

**What it is:** home, Install, Getting started, Testing, vusb, UI, and the
Docs index — plus the two hand-written reference pages (`cli.md`, `usb.md`).

**Approach:** standard Hugo per-language content — `content/zh/install.md` and
friends. The prose is translated; **code, commands, flags, file paths, driver
ids, and the captured terminal output are not.** The terminal blocks stay
byte-for-byte identical across languages (that is the point of "real output, not
typed by hand"); only the surrounding sentences change.

**Home page wrinkle:** the home page prose lives in `layouts/index.html`, not
`content/_index.md` (which holds only the title). To translate it as content,
move the home prose into `content/_index.md` and let the template render
`.Content`, or treat it as i18n strings. This is a small refactor worth doing as
part of scaffolding — it also makes the home page a normal translatable page
instead of a special case.

**Feasibility:** fully feasible. ~3,100 words × six languages is the bulk of the
human-translation effort, but it is a one-time cost and the pages are stable.

### Layer 3 — Generated driver facts (table + per-driver pages)

**What it is:** the driver table and each driver page are rendered from
`data/drivers.json`, which is generated at build time from the oxrok repo
(`tools/site-data`, reading `docs/drivers.toml`). The human-written prose in
there is: `name` (mostly proper nouns), `reason` (one line per not-ported
driver), and `evidence`, `behaviour`, `limits` (free prose per ported driver),
plus firmware `note`/`source`. Everything else — ids, models, kind, connection,
status, `show` output, cases, coverage — is data or machine output and is not
translated.

**The constraint, stated plainly.** "Generated, not written" means the English
facts come from the repo at build time so they cannot go stale. A translation
checked into the *website* repo by hand would violate the same principle: it
would drift from the English source the moment `drivers.toml` changes, and it
would be hand-maintained in exactly the way the ethos forbids.

So the translation must itself be **generated and checked**, not hand-placed
next to the English. Concretely:

- The English `data/drivers.json` stays the single source of truth, generated
  as today.
- A translation overlay lives in the website repo — `translations/zh/drivers.json`
  (and so on) — keyed by driver `key` + field (or, better, keyed by the exact
  English source string, so identical strings like "compares with libsigrok on
  an emulated device" are translated once and reused).
- A small build step (`tools/apply-translations.py`, alongside
  `gen-driver-pages.py`) merges the overlay onto the generated English data and
  emits `data/<lang>/drivers.json`. Templates render the localized field when
  present, else the English field.
- A completeness check reports every English prose string that has no
  translation in each language, so nothing can silently ship untranslated while
  still claiming a language is live.

**Vocabulary vs. prose.** The status/kinds/connection labels and the section
headings are fixed vocabulary and go through i18n (§5 Layer 1). The
`evidence`/`behaviour`/`limits`/`reason` sentences go through the overlay. The
`name` field is deliberately **not translated**: it is what a user matches
against `oxrok -L` and the model names behind `serial-dmm`, and translating
"Serial multimeters" to シリアルマルチメータ would not break anything but also
buys little. If the owner wants a localized display title, add a separate
localized summary string rather than renaming the driver.

**Feasibility:** the *mechanism* is straightforward and preserves the ethos. The
*content* is the long tail: ~900 words today, growing every time `drivers.toml`
gains a behaviour or limit. This is the layer where the maintenance story in §7
matters most.

### Layer 4 — Reference docs

**What it is:** `decoders.md` is copied from the oxrok repo's `DECODERS.md` on
every build (by `tools/import-docs.py`); `cli.md` and `usb.md` are hand-written
for the site.

**Recommendation:** leave the reference docs in English for every locale,
initially. Three reasons:

- They are developer-facing; the developer audience reads English, and these
  are the lowest-value pages to localize for the site's primary audience.
- `decoders.md` is regenerated from the repo every release, so translating it
  means maintaining a translation overlay that tracks a moving target (§6
  mechanism would apply) — real work for the least-read page.
- The nav already frames Docs as reference; a "reference stays in English" note
  is honest and common.

If the owner later wants them translated, `cli.md`/`usb.md` become normal
per-language content, and `decoders.md` uses the same overlay + completeness
check as the driver prose, keyed to the imported source. Nothing in the
architecture prevents it; it is deferred, not abandoned.

The **blog** is English-only for now (no posts exist), which is fine.

---

## 6. The "generated, not written" translation model

This is the one place the plan could go wrong, so it is worth a section.

The site already enforces "generated, not written" with two mechanisms, and
translations reuse the same ideas:

1. **English is always correct and always ships.** `make` regenerates
   `data/drivers.json` and the docs from the oxrok checkout on every release and
   on the daily schedule. That must not be blocked on translations — a new oxrok
   release must deploy even if a translation lags. So translations are
   *derived* from English and are *never* allowed to block the English build.

2. **Translations are keyed to the English source and verified against it.**
   The overlay maps source strings → translated strings. The build check diffs
   English against each overlay and reports missing/stale entries. A stale entry
   (an English string whose wording changed, leaving an orphaned translation) is
   detected the same way, not left to rot.

3. **A language is "live" only when it is complete enough.** Rather than a hard
   fail, the policy is: fall back to English for anything untranslated, and
   surface a per-language completeness number. A language appears in the
   switcher only once its chrome + core pages + driver prose hit a stated
   threshold (e.g. 100% of chrome and core pages, 95%+ of driver prose). Below
   that it is not advertised. This keeps the honesty of the table ("how far can
   I trust this") intact in every language, and avoids half-translated nav.

The alternative — putting translated fields inside `docs/drivers.toml` in the
oxrok repo — is rejected: it couples translation to the code repo, makes
translators work in a checkout of the tool, and bloats a file whose purpose is
"one place a person maintains driver facts." The website repo is the right home
for translations; the oxrok repo stays the source of facts.

---

## 7. Keeping translations in sync over time

The site regenerates data and docs on every release and every day. English
changes in three ways:

- **Driver prose changes** when `drivers.toml` changes (new port, new behaviour,
  corrected limit, a hardware report turned into a `hardware` status).
- **Reference docs change** when `DECODERS.md` changes (deferred — stays English).
- **Chrome and hand-written pages change** when the owner edits the site.

The workflow for each:

- **Chrome + vocabulary.** Tiny, stable catalogs. A CI check (or a
  `tools/check-i18n.py`) fails if any `i18n/<lang>.toml` is missing a key that
  `en.toml` has. Changes are rare and reviewed by eye.
- **Hand-written pages.** The owner edits the English page; the translation
  lags until a translator (human or MT-assisted) updates the `content/<lang>/`
  copy. Because pages are short and change slowly, this is a normal
  documentation task, not a pipeline.
- **Driver prose.** The build's translation delta is the control loop. On each
  release, the completeness check lists every English `evidence`/`behaviour`/
  `limits`/`reason` string that is new or reworded. The owner runs those through
  a translation memory + machine translation, reviews, and commits the additions
  to the overlays. Because strings are short and many repeat verbatim across
  drivers, a **translation memory** (a simple JSON or PO file keyed by source
  string) means "compares with libsigrok on an emulated device" is translated
  once, not per driver.

**Machine translation vs. human.** Recommendation: human-written (or
human-edited) for the chrome and the core hand-written pages, which are small,
stable, and are the first thing every visitor reads; machine translation with a
human spot-check for the long tail of driver prose. This is consistent with the
site's own disclosure — it already says plainly it was "written by an LLM,
directed by a person." Extend that honesty to translations: a footer note (or
`<meta name="generator">`) can say non-English prose is machine-assisted and
reviewed. The ethos survives translation if we say what was machine-made rather
than pretend it was not.

**Where the steps live in the build.** Add a `translations` target to the
`Makefile` (runs `tools/apply-translations.py` and `tools/check-i18n.py`) wired
into `all`, so `make` produces localized data and verifies coverage in the same
run that regenerates English. The deploy workflow is unchanged in shape.

---

## 8. Search across languages

Search is Pagefind, run once over the built HTML (`pagefind -s public`). One
index covers all languages, but it must be told the language of each page so it
can segment text correctly — this matters especially for Chinese and Japanese,
which have no spaces between words.

- **Tag pages:** add `data-pagefind-lang="{{ .Site.Language.Lang }}"` to the
  `<html>` element (or the search element) so Pagefind knows each page's
  language. Pagefind's language support handles CJK segmentation when the
  language is declared.
- **Declare the languages:** a `pagefind.yml` (or `--languages` flag) listing
  `en, zh, ja, es, fr, de` (plus `ru, ko` later) so the index is built
  multilingual. Verify the exact flag against the pinned Pagefind v1.6.0.
- **Scope results:** each page's `new PagefindUI(...)` is given
  `mergeFilter: { language: currentLang }` so a visitor searching on the French
  site gets French results by default, and a `translations` object for the UI
  strings ("Search", "Loading…", the empty state). A cross-language toggle is
  optional; default to same-language-only, which is what people expect.

The **device table's own filter/search** (`data-search` on each row) is
client-side and already language-independent: it matches against the untranslated
driver name, ids, and model list, which is exactly what should be searched
("UT61E" must find `serial-dmm`). No change.

---

## 9. Phased rollout and cost

Costs are rough person-effort: one-time engineering is in the site, recurring
translation is per language. Translation effort scales with the *six* (later
eight) languages; engineering is paid once.

**Phase 0 — Multilingual scaffolding, no new content.**
Hugo config, `lang`/`dir` attributes, language switcher, hreflang, sitemap and
robots, Pagefind language tagging and scoping, and the `i18n/` catalog mechanism
with English as the only entry. English output is byte-for-byte identical to
today (same URLs, same pages), so this ships with no visible change and no
regression risk. *Engineering: small (a few days). Translation: none.*

**Phase 1 — UI chrome + vocabulary in all six languages.**
Translate nav/footer/buttons, status names and definitions, kinds, connections,
column headers, filter labels. The device table and driver pages are fully
readable in-language; driver prose still falls back to English. This alone
answers "does it work with my device, and how far can I trust that" in-language.
*Engineering: small. Translation: small (~200 strings × 6), human-reviewed.*

**Phase 2 — Hand-written pages in all six languages.**
Home (after moving its prose out of the template), Install, Getting started,
Testing, vusb, UI, Docs index, plus `cli.md`/`usb.md`. A language is not shown
in the switcher until Phase 2 for that language is done, so the nav never points
at half-translated pages. *Engineering: small (the home-page refactor).
Translation: medium (~3,100 words × 6).*

**Phase 3 — Generated driver prose in all six languages.**
The overlay + completeness check from §6, plus the translation-memory/delta
workflow from §7. This is the long tail and the ongoing cost. *Engineering:
medium (overlay tooling + check). Translation: medium now (~900 words × 6),
recurring and small each release.*

**Phase 4 — Reference docs, and the second language wave.**
Translate `cli.md`/`usb.md`/`decoders.md` if the owner wants (recommend deferring
`decoders.md`), and add Russian and Korean, which are cheap once the pipeline and
CJK handling exist. *Engineering: small. Translation: medium per item.*

**Deferred / not doing:** blog translation, Arabic (RTL) until RTL is wanted,
Portuguese/Italian/Hindi until there is evidence of demand.

Summary table:

| Phase | Engineering | Translation | Risk |
|---|---|---|---|
| 0 Scaffolding | small | none | low — must keep English identical |
| 1 Chrome + vocab | small | small × 6 | low |
| 2 Hand pages | small | medium × 6 | low-medium — home refactor |
| 3 Driver prose | medium | medium × 6, then small/cycle | medium — the sync loop |
| 4 Docs + ru/ko | small | medium per item | low |

The expensive, ongoing cost is **not** the initial translation — it is Phase 3's
delta loop (a few new or reworded driver strings on most oxrok releases) and the
human review that should accompany it. For a single maintainer, that is the
thing to size before committing to all six languages on day one.

---

## 10. Risks and gotchas

- **English must stay byte-identical through Phase 0.** The switcher, hreflang,
  and per-language content are additive; any change to English URLs or markup
  breaks existing links and search. Phase 0 is verified by diffing the built
  English site against the pre-i18n build.
- **Code, commands, and output are never translated.** The terminal blocks and
  the `--show` capability dumps stay LTR and verbatim. Only the prose around
  them changes. Getting this wrong breaks copy-paste instructions.
- **The `dict` lookups for status/kind/connection** key on raw English values.
  The i18n change must keep the key and swap only the label, or filters and
  badges break.
- **The emulator SVG** (`layouts/partials/emulator.html`) has English text baked
  into the picture, plus an `aria-label`. Translating SVG text is fiddly; the
  pragmatic path is to translate the `aria-label` and the surrounding prose and
  leave the diagram's labels, or to move its labels into the template. Flag as a
  small decision, not a blocker.
- **CJK rendering.** No web fonts needed, but verify line-height and that long
  Japanese/Chinese words wrap sanely (`word-break`/`overflow-wrap`); the system
  CJK fonts handle glyphs, the CSS may need a `lang`-aware tweak. Korean and
  Chinese are covered by the same work.
- **Pagefind CJK.** Chinese and Japanese are useless to search unless the page
  language is declared so Pagefind segments correctly. This is easy to miss and
  worth an explicit smoke test ("search デモ returns the demo page").
- **Budget check.** `tools/check.py` fails any page over 100 KB. CJK text is
  dense but the pages are short; the check already guards this. No action beyond
  keeping it.
- **The honesty disclosures** ("written by an LLM, directed by a person";
  "most drivers have never met their device") must survive translation, and
  machine-assisted translation should be disclosed the same way.

---

## 11. Open questions / decisions for the owner

1. **Language order.** Ship the six first, or start with two (zh + ja) to prove
   the pipeline before paying for es/fr/de? Recommendation: scaffold with six
   defined, but translate in a sensible order (zh, ja, es, fr, de) so early
   effort concentrates on the languages with the most non-English hardware
   hobbyists.
2. **Chinese variant.** Simplified only (recommended), or Simplified and
   Traditional as two separate languages later?
3. **Completion gate.** Confirm the policy "a language is advertised only when
   its chrome + core pages + driver prose are complete, with English fallback
   otherwise" — versus a stricter "no fallback, ever" (which would block
   releases on translation lag; not recommended).
4. **Machine translation disclosure.** Are you comfortable with a footer note
   that non-English prose is machine-assisted and human-reviewed (consistent
   with the existing LLM disclosure), or should every translated string be
   human-written? The latter raises Phase 2–3 cost significantly.
5. **Reference docs.** Confirm they stay English in all locales initially, with
   the overlay mechanism available later.
6. **Search scoping.** Same-language-only search results (recommended), or a
   cross-language toggle?
7. **Who reviews translations.** This is a one-person project so far; for the
   six (later eight) languages, is review by you (spot-check) acceptable, or do
   you want a trusted native speaker per language? This is the real determinant
   of the recurring cost in Phase 3.
8. **Switcher form.** A `<select>` in the header, or native-name links in the
   footer (or both)?

---

## 12. What "done" looks like

- `/`, `/devices/`, `/install/`, … are byte-identical to today in English.
- `/zh/`, `/ja/`, `/es/`, `/fr/`, `/de/` serve the same site, with the chrome,
  status table, and core pages in-language, driver prose in-language where
  translated, English where not, and no translated command or machine output.
- The switcher moves between languages per page, hreflang and sitemap are
  correct, and search returns results in the page's language.
- Every release regenerates English facts and re-checks translations against
  them, surfacing exactly the strings that changed, so translations can never
  silently go stale.
- The ethos holds in every language: facts are generated, not written, and the
  site still says plainly what was checked how.
