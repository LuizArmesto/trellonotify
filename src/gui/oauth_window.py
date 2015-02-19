# -*- coding: utf-8 -*-

import urlparse

import oauth2 as oauth
from gi.repository import GObject
from gi.repository import Gtk

from gui.oauth_view import OAuthView
from gui.oauth_view import TrelloMixin


class OAuthViewTrello(OAuthView, TrelloMixin):
    pass


class OAuthWindowTrello(Gtk.Window):

    def __init__(self, consumer_key=None, consumer_secret=None, app_name='',
            request_token_url=None, authorize_url=None, access_token_url=None):
        super(OAuthWindowTrello, self).__init__(type=Gtk.WindowType.TOPLEVEL)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(800, 600)
        self.connect('destroy', self.on_quit)

        self.oauthview = OAuthViewTrello(consumer_key, consumer_secret, 
                app_name,
                request_token_url, authorize_url, access_token_url)
        self.add(self.oauthview)

        self.oauthview.connect('access-allowed', self.on_allowed)
        self.oauthview.connect('access-denied', self.on_denied)

        self.show_all()

    def request_access(self):
        self.oauthview.request_access()

    def on_denied(self, widget, resp):
        self.hide()
        self.emit('access-denied', resp)

    def on_allowed(self, widget, resp):
        self.hide()
        self.emit('access-allowed', resp)

    def on_quit(self, widget):
        #TODO: Should not end main loop
        Gtk.main_quit()

GObject.signal_new('access-allowed', OAuthWindowTrello,
                    GObject.SIGNAL_RUN_LAST,
                    GObject.TYPE_NONE,
                    (GObject.TYPE_PYOBJECT,))

GObject.signal_new('access-denied', OAuthWindowTrello,
                    GObject.SIGNAL_RUN_LAST,
                    GObject.TYPE_NONE,
                    (GObject.TYPE_PYOBJECT,))

