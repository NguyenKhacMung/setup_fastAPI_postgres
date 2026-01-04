from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, text
from alembic import context
from app.core.config import settings

# Alembic Config object
config = context.config

# .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
import app.models  # models/__init__.py

from sqlmodel import SQLModel

target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
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
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def get_tenant():
    return context.get_x_argument(as_dictionary=True).get("tenant")


def process_revision_directives(context, revision, directives):
    tenant = get_tenant()
    if tenant:
        directives[0].version_path = "alembic/versions/tenant"
    else:
        directives[0].version_path = "alembic/versions/master"


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    tenant_schema = get_tenant()
    with connectable.connect() as connection:

        if tenant_schema:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant_schema}"))
            connection.execute(text(f'SET search_path TO "{tenant_schema}"'))
            connection.commit()

            def include_object(object, name, type_, reflected, compare_to):
                if type_ == "table" and name == "alembic_version":
                    return False

                if type_ == "table":
                    return object.schema is None

                return True

            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                version_table_schema=tenant_schema,
                include_schemas=True,
                include_object=include_object,
                process_revision_directives=process_revision_directives,
            )

            with context.begin_transaction():
                context.run_migrations()

        else:
            connection.execute(text("CREATE SCHEMA IF NOT EXISTS master"))
            connection.commit()

            def include_object(object, name, type_, reflected, compare_to):
                if type_ == "table":
                    return object.schema == "master"
                return True

            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                version_table_schema="master",
                include_schemas=True,
                include_object=include_object,
                process_revision_directives=process_revision_directives,
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
