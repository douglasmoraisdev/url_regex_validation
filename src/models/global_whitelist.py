from sqlalchemy import (
    Table,
    MetaData
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, MetaData

from .connectors.mysqldb import MySQLDBConnection
from utils.log_utils import log

Base = declarative_base()


class _GlobalWhitelist(Base):
    __tablename__ = 'global_whitelist'

    id_regex = Column(Integer, primary_key=True)
    regex = Column(String)

class GlobalWhitelistModel():

    def __init__(self):
        self.engine = MySQLDBConnection().connection
        self.log = log


    def get_whitelist(self, args):
        session = Session(self.engine)

        try:
            query = session.query(_GlobalWhitelist).all()

            return query

        except Exception as e:
            self.log.error('Exception on query [global] [%s]' % str(e))
            return False
        finally:
            session.close()
        return True

    def insert_global_regex(self, regex):
        session = Session(self.engine)

        try:
            session.add(_GlobalWhitelist(regex=regex))
            session.commit()
        except Exception as e:
            self.log.error('Exception on insert regex [global] [%s]' % str(e))
            return False
        finally:
            session.close()
        return True
