# -*- coding: utf-8 -*-

__all__ = ['Trello']

from .models import Board
from .models import Card
from .models import Checklist
from .models import List
from .models import Member
from .models import Notification
from .models import Organization
from .models import Token

from .providers import ApiOne


class BaseTrello(object):
    """
    Represents Trello
    """

    def __init__(self, *args, **kwargs):
        super(BaseTrello, self).__init__(*args, **kwargs)

    @property
    def token(self):
        return Token(self, self.oauth_token)

    @property
    def me(self):
        return self.get_member('me')

    def get_board(self, id_, model=Board):
        return model(self, id_)

    def get_card(self, id_, model=Card):
        return model(self, id_)

    def get_checklist(self, id_, model=Checklist):
        return model(self, id_)

    def get_list(self, id_, model=List):
        return model(self, id_)

    def get_member(self, id_, model=Member):
        return model(self, id_)

    def get_notification(self, id_, model=Notification):
        return model(self, id_)

    def get_organization(self, id_, model=Organization):
        return model(self, id_)


class Trello(BaseTrello, ApiOne):
    pass
