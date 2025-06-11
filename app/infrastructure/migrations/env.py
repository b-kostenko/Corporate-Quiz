from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from alembic.script import ScriptDirectory

from app.infrastructure.postgres.models.base import BaseModelMixin
from app.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = BaseModelMixin.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# A helper function to set custom revision IDs
def process_revision_directives(context, revision, directives):
    migration_script = directives[0]
    # Extract current head revision
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()

    if head_revision is None:
        # Case of the first migration
        new_rev_id = 1
    else:
        # Increment revision number
        last_rev_id = int(head_revision.lstrip("0"))
        new_rev_id = last_rev_id + 1

    # Add leading zeros: e.g. 1 -> 00001
    migration_script.rev_id = f"{new_rev_id:05}"


# Offline mode: no active database connection
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Online mode: active database connection
async def run_migrations_online():
    """Run migrations in 'online' mode."""
    engine = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    # Properly dispose the engine to close all connections
    await engine.dispose()


# Synchronous wrapper for migrations
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )
    with context.begin_transaction():
        context.run_migrations()


# Main execution logic
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    import platform

    # Ensure compatibility with Windows event loops
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(run_migrations_online())
