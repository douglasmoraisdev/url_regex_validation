#!/usr/bin/env python3
from os import getenv
from pathlib import Path
import sys

from sqlalchemy.orm import Session
import alembic.config
from dotenv import load_dotenv

from models.connectors.mysqldb import MySQLDBConnection

engine = MySQLDBConnection().migration_connection_from_dotenv()

load_dotenv()


def show_help():
    print('''
          Usage:
          $ ./prepare.py 
             Create database and tables from .env(Production).

          $ ./prepare.py -tests  
             Create database and tables from tests/.env(Test Suit).

          $ ./prepare.py -help  
             Show this help.
            '''
          )

# migration env and help
if len(sys.argv) > 1:
    if sys.argv[1] == '-tests':
        load_dotenv(dotenv_path='tests/.env', override=True)
    if sys.argv[1] == '-help':
        show_help()
        sys.exit()

# create mysql schemas
session = Session(engine)
session.execute(f"CREATE SCHEMA IF NOT EXISTS {getenv('MYSQL_DB_SCHEMA')}")

# run alembic migration
alembicArgs = [
    '--raiseerr',
    'upgrade', 'head',
]
alembic.config.Config('./alembic.ini')

alembic.config.main(argv=alembicArgs)

# create required paths
Path("log").mkdir(exist_ok=True)

print('DONE!')