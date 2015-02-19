# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OAuth(Base):
    __tablename__ = 'oauth'

    id = Column(Integer, primary_key=True)
    consumer_key = Column(Text)
    consumer_secret = Column(Text)
    token = Column(Text)
    token_secret = Column(Text)

    def __init__(self, consumer_key, consumer_secret, token, secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token = token
        self.token_secret = secret

    def __repr__(self):
        return self.name

