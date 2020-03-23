from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from os import getenv, path
from dotenv import load_dotenv

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

load_dotenv()

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url.format(
            MYSQL_DB_USER=getenv('MYSQL_DB_USER'),
            MYSQL_DB_PASSWORD=getenv('MYSQL_DB_PASSWORD'),
            MYSQL_DB_HOST=getenv('MYSQL_DB_HOST'),
            MYSQL_DB_PORT=getenv('MYSQL_DB_PORT'),
            MYSQL_DB_SCHEMA=getenv('MYSQL_DB_SCHEMA')),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    cfg = config.get_section(config.config_ini_section)

    cfg['sqlalchemy.url'] = cfg['sqlalchemy.url'].format(
        MYSQL_DB_USER=getenv('MYSQL_DB_USER'),
        MYSQL_DB_PASSWORD=getenv('MYSQL_DB_PASSWORD'),
        MYSQL_DB_HOST=getenv('MYSQL_DB_HOST'),
        MYSQL_DB_PORT=getenv('MYSQL_DB_PORT'),
        MYSQL_DB_SCHEMA=getenv('MYSQL_DB_SCHEMA'))

    connectable = engine_from_config(cfg)

    with connectable.connect() as connection:
        
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
