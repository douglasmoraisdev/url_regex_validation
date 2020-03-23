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

class _ClientWhitelist(Base):

    __tablename__ = 'client_whitelist'

    id_regex = Column(Integer, primary_key=True)
    client = Column(String)
    regex = Column(String)

class ClientWhitelistModel():

    def __init__(self):
        self.engine = MySQLDBConnection().connection
        self.log = log

    def get_whitelist(self, args):
        session = Session(self.engine)

        try:
            query = session.query(_ClientWhitelist).filter(
                _ClientWhitelist.client == args['client']).all()

            return query

        except Exception as e:
            self.log.error('Exception on query [client] [%s]' % str(e))
            return False
        finally:
            session.close()
        return True

    def insert_client_regex(self, client, regex):
        session = Session(self.engine)

        try:
            session.add(_ClientWhitelist(client=client,
                                         regex=regex))
            session.commit()
        except Exception as e:
            self.log.error('Exception on insert regex [client] [%s]' % str(e))
            return False
        finally:
            session.close()
        return True
