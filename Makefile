# oxrok.dev build
#
# The site describes a checkout of oxrok. OXROK is that checkout; it defaults
# to ~/oxrok. The build generates data/drivers.json from it (via the oxrok
# repo's tools/site-data, so the generator changes with what it reads),
# generates the per-driver page stubs, builds with Hugo, and indexes with
# Pagefind.

OXROK ?= $(HOME)/oxrok
HUGO ?= hugo
PAGEFIND ?= pagefind

.PHONY: all data pages docs hugo pagefind check clean

all: data pages docs hugo pagefind check

data:
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

clean:
	rm -rf public pagefind
