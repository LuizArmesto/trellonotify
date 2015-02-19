## Process this file with automake to produce Makefile.in

trellonotify_libdir = $(pythondir)/trellonotify/lib
trellonotify_lib_PYTHON = \
	__init__.py \
	common.py \
	dal.py \
	defs.py \
	trello.py

defs.py: defs.py.in
	sed						\
		-e s!\@datadir\@!$(datadir)!		\
		-e s!\@VERSION\@!$(VERSION)!		\
		< $< > $@
defs.py: Makefile

CLEANFILES = defs.py
EXTRA_DIST = defs.py.in

DISTCLEANFILES = \
	$(CLEANFILES)

