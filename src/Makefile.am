## Process this file with automake to produce Makefile.in

SUBDIRS = db gui lib

trellonotifydir = $(pythondir)/trellonotify
trellonotify_PYTHON = \
	__init__.py \
	notifier.py \

uninstall-hook:
	rm -fr $(trellonotify)
