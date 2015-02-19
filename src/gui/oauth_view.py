# -*- coding: utf-8 -*-

import urlparse

import oauth2 as oauth

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import WebKit


class TrelloMixin(object):

    request_token_url = 'https://trello.com/1/OAuthGetRequestToken'
    authorize_url = 'https://trello.com/1/OAuthAuthorizeToken'
    access_token_url = 'https://trello.com/1/OAuthGetAccessToken'

    def on_load(self, webview, webframe, finished=False):
        dom = self.dom
        url = self.url
        if 'token/approve' in url:
            pre = dom.get_elements_by_tag_name('pre')
            if pre and pre.get_length() > 0:
                self.oauth_verifier = pre.item(0).get_inner_text().strip()
                self.hide()
        elif url.endswith('trello.com/'):
            self.on_denied()

    def goto_authorize_url(self):
        url = '{}?oauth_token={}&name={}&scope=read,write&expiration=never'.format(
                self.authorize_url,
                self.request_token['oauth_token'],
                self.app_name.replace(' ', '+'))
        self.goto(url)


class OAuthView(WebKit.WebView):

    def __init__(self, consumer_key=None, consumer_secret=None, app_name='',
            request_token_url=None, authorize_url=None, access_token_url=None):
        super(OAuthView, self).__init__()

        self.app_name = app_name

        if request_token_url:
            self.request_token_url = request_token_url
        if authorize_url:
            self.authorize_url = authorize_url
        if access_token_url:
            self.access_token_url = access_token_url

        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.client = oauth.Client(self.consumer)

        self.connect('load-committed', self.on_load)
        self.connect('load-finished', self.on_load, True)

        self.show_all()

    def request_access(self):
        self.fetch_request_token()

    def fetch_request_token(self):
        resp, content = self.client.request(self.request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])
        self.request_token = dict(urlparse.parse_qsl(content))

    def fetch_access_token(self):
        token = oauth.Token(self.request_token['oauth_token'],
                            self.request_token['oauth_token_secret'])
        token.set_verifier(self.oauth_verifier)
        client = oauth.Client(self.consumer, token)

        resp, content = client.request(self.access_token_url, "POST")
        self.access_token = dict(urlparse.parse_qsl(content))

    def goto(self, url):
        if url:
            self.load_uri(url)

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, value):
        self.__access_token = value
        self.on_allowed()

    @property
    def request_token(self):
        return self.__request_token

    @request_token.setter
    def request_token(self, value):
        self.__request_token = value
        self.goto_authorize_url()

    @property
    def oauth_verifier(self):
        return self.__oauth_verifier

    @oauth_verifier.setter
    def oauth_verifier(self, value):
        self.__oauth_verifier = value
        self.fetch_access_token()

    @property
    def url(self):
        return self.get_uri()

    @property
    def dom(self):
        return self.get_dom_document()

    def on_denied(self):
        # TODO: Display failed message
        self.emit('access-denied', {})

    def on_allowed(self):
        # TODO: Display successful message
        self.emit('access-allowed', self.access_token)


GObject.signal_new('access-allowed', OAuthView,
                    GObject.SIGNAL_RUN_LAST,
                    GObject.TYPE_NONE,
                    (GObject.TYPE_PYOBJECT,))

GObject.signal_new('access-denied', OAuthView,
                    GObject.SIGNAL_RUN_LAST,
                    GObject.TYPE_NONE,
                    (GObject.TYPE_PYOBJECT,))


