# oxrok.dev build
#
# The site describes a checkout of oxrok. OXROK is that checkout, always
# the sibling directory ../oxrok. The build generates data/drivers.json
# from it (via the oxrok repo's tools/site-data, so the generator changes
# with what it reads), generates the per-driver page stubs, builds with
# Hugo, and indexes with Pagefind.

OXROK := ../oxrok
HUGO ?= hugo
PAGEFIND ?= pagefind

.PHONY: all data pages docs hugo pagefind check serve clean

all: data pages docs hugo pagefind check

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
