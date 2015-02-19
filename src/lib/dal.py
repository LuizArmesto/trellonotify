# -*- coding: utf-8 -*-

import os

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, eagerload
    from sqlalchemy.orm.exc import NoResultFound
except ImportError:
    print "Please install SQLAlchemy!"
    raise SystemExit

from xdg.BaseDirectory import *

from db.entities import OAuth
from lib.common import DB_NAME
from lib.common import APP_SHORTNAME


class DAL(object):

    def __init__(self, sessionmaker=sessionmaker, enginemaker=create_engine, 
            app_name=APP_SHORTNAME, db_name=DB_NAME, fake=False):
        self.new_setup = False
        self.sessionmaker = sessionmaker
        self.enginemaker = enginemaker
        self.app_name = app_name
        self.db_name = db_name
        self.is_fake = fake

        self.init_data_dir()        
        self.create_session()
        self.create_tables()
        if self.new_setup:
            self.create_default_values()
    
    def init_data_dir(self):
        self.data_dir = os.path.join(xdg_data_home, self.app_name.lower())
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)
            # Safe to assume that this is a new setup.
            self.new_setup = True

    def create_session(self):
        # The fake mode is used to run tests using a clean db created on memory
        if not self.is_fake:
            self.engine = self.enginemaker('sqlite:///{}'.format(
                    os.path.join(self.data_dir, self.db_name)))
        else:
            self.engine = self.enginemaker('sqlite:///:memory:', echo=False)
        self.Session = self.sessionmaker(bind=self.engine)

    def create_tables(self):
        OAuth.metadata.create_all(self.engine)

    def create_default_values(self):
        pass

    def add(self, obj):
        session = self.Session()

        if isinstance(obj, OAuth):
            dbobj = obj
            try:
                instance = session.query(OAuth).filter_by(id=dbobj.id).one()
                if instance:
                    # TODO: Make this generic
                    instance.consumer_key = dbobj.consumer_key
                    instance.consumer_secret = dbobj.consumer_secret
                    instance.token = dbobj.token
                    instance.token_secret = dbobj.token_secret

                if session.dirty:
                    session.commit()

                dbobj_id = instance.id

            except NoResultFound, e:
                session.add(dbobj)
                session.commit()
                dbobj_id = dbobj.id
            except Exception, e:
                session.rollback()
                print str(e)
            finally:
                session.close()

