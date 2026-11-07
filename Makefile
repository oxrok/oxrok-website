# oxrok.dev build
#
# The site describes a checkout of oxrok. OXROK is that checkout, always
# the sibling directory ../oxrok. The build generates data/drivers.json
# from it (via the oxrok repo's tools/site-data, so the generator changes
# with what it reads), generates the per-driver page stubs, builds with
# Hugo, and indexes with Pagefind.
#
# The UI screenshots come from the oxrok-ui checkout, UI (the sibling
# ../ui). They are regenerated on every UI release; `make ui` copies them
# into static/ui/ and records which release they came from in data/ui.json.
# To keep them in sync after a UI release: `make ui`, then commit
# static/ui/ and data/ui.json. The build runs it too, so the deployed site
# carries the release's screenshots.

OXROK := ../oxrok
UI ?= ../ui
HUGO ?= hugo
PAGEFIND ?= pagefind

.PHONY: all build ui data pages docs hugo pagefind check serve clean

all: ui data pages docs hugo pagefind check

# `build` is an alias for `all`: everything short of serving.
build: all

# Copy the UI screenshots from $(UI) into static/ui/ and write data/ui.json.
ui:
	python3 tools/sync-ui.py $(UI)

data:
	mkdir -p data
	python3 $(OXROK)/tools/site-data $(OXROK) > data/drivers.json

pages: data
	python3 tools/gen-driver-pages.py

docs:
	python3 tools/import-docs.py $(OXROK)

hugo: data pages docs
	$(HUGO)

pagefind:
	$(PAGEFIND) -s public

# Checks the built site: generated data valid, every driver has a status,
# no broken links, no page over budget, no libsigrok-bug mentions.
check:
	python3 tools/check.py

# Build everything (including the checks), then serve public/ at
# http://localhost:8080 — the exact tree that gets deployed, Pagefind
# included. Ctrl-C to stop.
serve: all
	python3 -m http.server -d public 8080

clean:
	rm -rf public pagefind
