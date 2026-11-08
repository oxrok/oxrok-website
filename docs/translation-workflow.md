# Translation workflow (agent instructions)

How the site's translations are made and kept in sync. These are instructions
for any agent or person touching translated content. The rule of thumb:

> Always start from English. Find what changed in English. Translate exactly
> that, in every other language, in the same step.

English is the source of truth. A translation is never written from scratch,
never written from another language, and never touched without first looking at
the English it renders.

## The order, every time

1. **English first.** Any new or changed string is first made correct in the
   English source. Then, and only then, is it translated.
2. **Find the delta.** Use `git diff` (or the last release vs. now) to list
   exactly what changed, filtered to English sources:
   - `content/*.md` and `content/docs/*.md` (hand-written pages)
   - `layouts/` (chrome and generated-page templates)
   - `i18n/en.toml` (the English copy of the UI-string catalog)
   - `data/drivers.json` (regenerated from `../oxrok/docs/drivers.toml` — the
     driver prose: `evidence`, `behaviour`, `limits`, `reason`, `firmware`)
3. **Follow with the other languages**, applying the same delta to each:
   - `i18n/<lang>.toml` — UI chrome and vocabulary
   - `content/<lang>/*.md` — hand-written pages
   - `translations/<lang>/drivers.json` — driver prose overlay
4. **Run the checks.** `make check` (and the i18n/translation completeness
   check) must pass. A language is committed only when its delta is at parity
   with the English delta that triggered it.

## Hard rules (apply to every language, every run)

- **Translate prose only.** Never translate, alter, or reorder: code, shell
  commands, flags, file paths, driver/decoder ids, model names, `--show` or
  `-L` output, or any captured terminal output. These stay verbatim and
  left-to-right in every language.
- **Names are not translated.** A driver `name` is what a user matches against
  `oxrok -L`; "search UT61E finds its driver" must keep working. Keep names,
  vendor names, and model names as-is.
- **Terminology stays consistent.** Use the translation memory/glossary so a
  repeated English string (e.g. "compares with libsigrok on an emulated device")
  always renders the same way. Do not paraphrase per occurrence.
- **Honesty disclosures survive translation.** "written by an LLM, directed by
  a person" and "most drivers have never met their device" are translated, not
  softened or dropped.
- **Machine translation is a first draft.** A human reviews before commit. The
  result is disclosed as machine-assisted, consistent with the site's existing
  LLM disclosure.
- **A translated string is keyed to its English source.** If the English wording
  changes, the old translation is stale and must be re-done against the new
  wording — not left orphaned.

## Language-specific notes

- **zh** is Simplified (`zh-Hans`). Traditional (`zh-Hant`) is a separate job,
  not in scope until asked.
- **CJK (zh, ja, ko):** no web fonts; the system font stack renders them. Keep
  line-height and word-wrap sane; don't insert spaces into CJK text.
- **Anything right-to-left (ar):** out of scope until RTL is decided.

## Where things live

| Content | English source | Translation |
|---|---|---|
| UI chrome, status/kind/connection labels | `i18n/en.toml` (keys) | `i18n/<lang>.toml` |
| Hand-written pages | `content/*.md`, `content/docs/*.md` | `content/<lang>/*.md` |
| Driver prose (`evidence`, `behaviour`, `limits`, `reason`) | `data/drivers.json` (from `../oxrok`) | `translations/<lang>/drivers.json` |
| Reference doc `decoders.md` | imported from `../oxrok/docs/DECODERS.md` | stays English (deferred) |

English is always regenerated and always ships. Translations are derived from it
and fall back to English where missing; a language is advertised only when it is
complete enough. See `docs/internationalization.md` for the full plan.
