# -*- coding: utf-8 -*-

__all__ = ['Attachment', 'Action', 'Board', 'Card', 'CheckItem', 'Checklist',
        'List', 'Member', 'Notification', 'Organization', 'Token']

from .base import Deletable
from .base import Model
from .base import Savable

from .fields import CollectionField
from .fields import DateTimeField
from .fields import Field
from .fields import JsonField
from .fields import ObjectField
from .fields import ReadOnlyField


class Attachment(Model):
    id = ReadOnlyField(is_local=True)

    bytes = Field()
    date = DateTimeField()
    id_member = Field()
    is_upload = Field()
    mime_type = Field()
    name = Field(display=True)
    previews = JsonField()
    url = Field()

    member = ObjectField(model='Member', ref='id_member')


class Action(Model, Deletable):
    _prefix = 'actions'

    id = Field(readonly=True, is_local=True)

    data = JsonField(readonly=True)
    date = DateTimeField(readonly=True)
    type = Field(readonly=True)

    board = ObjectField(model='Board')
    card = ObjectField(model='Card')
    list = ObjectField(model='List')
    member = ObjectField(model='Member')
    member_creator = ObjectField(model='Member')
    organization = ObjectField(model='Organization')


class Board(Model, Savable):
    _prefix = 'boards'

    id = Field(readonly=True, is_local=True)

    name = Field(required=True, display=True)
    desc = Field()
    closed = Field()
    subscribed = Field()
    id_organization = Field()
    prefs = JsonField()
    invited = Field(readonly=True)
    pinned = Field(readonly=True)
    url = Field(readonly=True)
    invitations = JsonField(readonly=True)  # TODO: Change to CollectionField
    memberships = JsonField(readonly=True)
    label_names = JsonField(readonly=True)

    actions = CollectionField(model='Action')
    cards = CollectionField(model='Card')
    checklists = CollectionField(model='Checklist', addable=('name',))
    lists = CollectionField(model='List', addable=('name', 'pos'))
    members = CollectionField(model='Member', addable=(('value', 'id'),),
            removable=True)
    cards = CollectionField(model='Card')
    members_invited = CollectionField(model='Member')
    organization = ObjectField(model='Organization', ref='id_organization')


class Card(Model, Savable, Deletable):
    _prefix = 'cards'

    id = ReadOnlyField(is_local=True)

    badges = JsonField()
    check_item_states = JsonField()
    closed = Field()
    desc = Field()
    due = DateTimeField()
    id_board = Field()
    id_checklists = JsonField()
    id_list = Field()
    id_members = JsonField()
    id_short = Field()
    id_attachment_cover = Field()
    manual_cover_attachment = Field()
    labels = JsonField()  # TODO: Convert to CollectionField?
    name = Field(display=True)
    pos = Field()
    subscribed = Field()
    url = Field()

    actions = CollectionField(model='Action')
    attachments = CollectionField(model='Attachment')
    board = ObjectField(model='Board', ref='id_board')
    checklists = CollectionField(model='Checklist', addable=(('value', 'id'),
            'name'), removable=True)
    list = ObjectField(model='List', ref='id_list')
    members = CollectionField(model='Member', addable=(('value', 'id'),),
            removable=True)
    members_voted = CollectionField(model='Member')


class CheckItem(Model):
    #TODO: Make this savable
    _prefix = None

    id = ReadOnlyField(is_local=True)

    name = Field(display=True)
    type = Field()
    pos = Field()
    state = Field()


class Checklist(Model):
    _prefix = 'checklists'

    id = ReadOnlyField(is_local=True)

    name = Field(display=True)
    id_board = Field()

    board = ObjectField(model='Board', ref='id_board')
    card = ObjectField(model='Card', ref='id_card')
    check_items = CollectionField(model='CheckItem', addable=(('value', 'id'),
        'name'), removable=True)


class List(Model):
    _prefix = 'lists'

    id = ReadOnlyField(is_local=True)

    name = Field(display=True)
    closed = Field()
    id_board = Field()
    pos = Field()
    subscribed = Field()

    actions = CollectionField(model='Action')
    board = ObjectField(model='Board', ref='id_board')
    cards = CollectionField(model='Card', addable=('name', 'desc'))


class Member(Model):
    _prefix = 'members'

    id = ReadOnlyField(is_local=True)

    bio = Field()
    full_name = Field(display=True)
    initials = Field()
    member_type = ReadOnlyField(lazy=True)
    status = ReadOnlyField()
    url = ReadOnlyField()
    username = ReadOnlyField()
    confirmed = ReadOnlyField(lazy=True)
    email = ReadOnlyField(lazy=True)
    trophies = ReadOnlyField(lazy=True)
    prefs = ReadOnlyField(lazy=True)

    actions = CollectionField(model='Action')
    boards = CollectionField(model='Board')
    boards_invited = CollectionField(model='Board')
    cards = CollectionField(model='Card')
    notifications = CollectionField(model='Notification')
    organizations = CollectionField(model='Organization')
    organizations_invited = CollectionField(model='Organization')
    tokens = CollectionField(model='Token')


class Notification(Model):
    _prefix = 'notification'

    id = ReadOnlyField(is_local=True)

    data = JsonField()
    date = DateTimeField()
    type = Field()
    unread = Field()

    board = ObjectField(model='Board')
    card = ObjectField(model='Card')
    list = ObjectField(model='List')
    member = ObjectField(model='Member')
    member_creator = ObjectField(model='Member')
    organization = ObjectField(model='Organization')


class Organization(Model):
    _prefix = 'organizations'

    id = ReadOnlyField(is_local=True)

    name = Field()
    display_name = Field(display=True)
    desc = Field()
    id_boards = JsonField()
    invited = Field()
    invitations = JsonField()
    memberships = JsonField()
    prefs = JsonField()
    power_ups = JsonField()
    url = Field()
    website = Field()
    logo_hash = Field()

    actions = CollectionField(model='Action')
    boards = CollectionField(model='Board')
    members = CollectionField(model='Member')
    members_invited = CollectionField(model='Member')


class Token(Model):
    _prefix = 'tokens'

    id = ReadOnlyField(is_local=True)

    identifier = Field()
    id_member = Field()
    date_created = DateTimeField()
    date_expires = DateTimeField()
    permissions = Field()

    member = ObjectField(model='Member', ref='id_member')

    def __init__(self, trello, id=None, *args, **kwargs):
        self.__hash = id
        super(Token, self).__init__(trello, id, *args, **kwargs)

    @property
    def path(self):
        # Should use the token hash instead of id to create tokens path.
        return '{}/{}'.format(self._prefix, self.__hash)
