from os import environ
from distutils.util import strtobool
from dotenv import load_dotenv

import sqlalchemy

load_dotenv()


class MySQLDBConnection:
    """MySQLDB Connection"""

    def __init__(self):
        self.connection = MySQLDBConnection.connection_from_dotenv()

    @staticmethod
    def connection_from_dotenv(encoding: str = 'utf-8'):
        connection_params: dict = dict(
            host=environ.get('MYSQL_DB_HOST', 'localhost'),
            port=int(environ.get('MYSQL_DB_PORT', 3306)),
            user=environ.get('MYSQL_DB_USER'),
            password=environ.get('MYSQL_DB_PASSWORD'),
            database=environ.get('MYSQL_DB_SCHEMA'),
            ssl=strtobool(str(environ.get('MYSQL_DB_SSL'))),
            encoding=encoding
        )
        return MySQLDBConnection.create_connection(connection_params)

    @staticmethod
    def migration_connection_from_dotenv(schema='', encoding: str = 'utf-8'):
        connection_params: dict = dict(
            host=environ.get('MYSQL_DB_HOST', 'localhost'),
            port=int(environ.get('MYSQL_DB_PORT', 3306)),
            user=environ.get('MYSQL_DB_USER'),
            password=environ.get('MYSQL_DB_PASSWORD'),
            database=schema,
            ssl=strtobool(str(environ.get('MYSQL_DB_SSL'))),
            encoding=encoding
        )
        return MySQLDBConnection.create_connection(connection_params)

    @staticmethod
    def create_connection(params: dict):

        connection_string = ''
        if params['database']:
            connection_string = "{type}+{engine}://{user}:{password}@{host}:{port}/{database}"
        else:
            connection_string = "{type}+{engine}://{user}:{password}@{host}:{port}"

        return sqlalchemy.create_engine(
            connection_string.format(
                host=params.get('host'),
                port=params.get('port', 3306),
                database=params.get('database'),
                user=params.get('user'),
                password=params.get('password'),
                type='mysql',
                engine='pymysql'
            ),
            pool_recycle=360,
            pool_size=20,
            max_overflow=0
        )


class MySQLDB:
    """ MySQLDB Connector """

    def __init__(self):
        self.conn = None

    @property
    def connector(self):
        if self.conn is None:
            self.conn = MySQLDBConnection()
        return self.conn

    def disconnect(self):
        self.connector.connection.close()
        self.conn = None

    def execute(self, query: str):
        return self.connector.connection.execute(query)
