# -*- coding: utf-8 -*-

from gi.repository import Gtk

from lib.common import APP_NAME
from lib.common import API_KEY
from lib.common import OAUTH_SECRET
from lib.trello import Trello
from lib.dal import DAL

from db.entities import OAuth

from gui.notification import NotificationManager
from gui.oauth_window import OAuthWindowTrello


class TrelloNotifier(object):
    def __init__(self, consumer_key=API_KEY, consumer_secret=OAUTH_SECRET,
            app_name=APP_NAME):
        self.__oauth_token = None
        self.__oauth_token_secret = None

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.app_name = app_name

        self.oauth_window = None  # Lazy

        self.init_dal()
        if self.oauth_token:
            self.init_trello()
        else:
            self.request_oauth_access()

    def init_dal(self):
        self.dal = DAL()

    def init_trello(self):
        self.trello = Trello(API_KEY, self.oauth_token)
        me = self.trello.me
        self.notification_manager = NotificationManager(me)

    @property
    def oauth_token(self):
        if not self.__oauth_token:
            saved_oauth = None
            try:
                session = self.dal.Session()
                q = session.query(OAuth)
                saved_oauth = q.first()
            except Exception, e:
                print str(e)
                pass
            finally:
                session.close()
            if saved_oauth:
                self.__oauth_token = saved_oauth.token
                self.__oauth_token_secret = saved_oauth.token_secret
        return self.__oauth_token

    @property
    def oauth_token_secret(self):
        return self.__oauth_token_secret

    def save_oauth_token(self, token):
        self.__oauth_token = token['oauth_token']
        self.__oauth_token_secret = token['oauth_token_secret']
        oauth_entity = OAuth(self.consumer_key, self.consumer_secret,
                self.oauth_token, self.oauth_token_secret)
        self.dal.add(oauth_entity)

    def request_oauth_access(self):
        if not self.oauth_window:
            self.oauth_window = OAuthWindowTrello(
                    self.consumer_key, self.consumer_secret, self.app_name)
            self.oauth_window.connect('access-denied', self.on_oauth_denied)
            self.oauth_window.connect('access-allowed', self.on_oauth_allowed)
        self.oauth_window.request_access()

    def on_oauth_allowed(self, window, token):
        self.save_oauth_token(token)
        self.init_trello()

    def on_oauth_denied(self, window, arg):
        pass


def main():
    app = TrelloNotifier()
    try:
        Gtk.main()
    except:
        Gtk.main_quit()


if __name__ == '__main__':
    main()
