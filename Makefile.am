## Process this file with automake to produce Makefile.in

SUBDIRS = src

bin_SCRIPTS = \
	trellonotify

CLEANFILES = \
	src/*/*.pyc \
	src/*/*.pyo

billreminder: trellonotify.in
	-sed -e s!\@PYTHONDIR\@!$(pythondir)! \
		< $< > $@

EXTRA_DIST = trellonotify.in
CLEANFILES += trellonotify

