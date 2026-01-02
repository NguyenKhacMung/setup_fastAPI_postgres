import os
import importlib
import pkgutil
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, text
from alembic import context
from sqlmodel import SQLModel

from app.core.config import settings

# --- 1. Load Config & Logging ---
config = context.config

# Hack: Convert async url to sync url for Alembic (nếu dùng asyncpg)
# Ví dụ: postgresql+asyncpg://... -> postgresql://...
db_url = str(settings.DATABASE_URL).replace("postgresql+asyncpg", "postgresql")
config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 2. Load Models (Quan trọng) ---
# Phải import đệ quy để SQLModel.metadata nhận diện được hết các bảng
import app.models

for loader, name, is_pkg in pkgutil.iter_modules(app.models.__path__):
    importlib.import_module(f"app.models.{name}")

target_metadata = SQLModel.metadata

# --- 3. Define Filter Functions (Bộ lọc bảng) ---


def include_object_master(object, name, type_, reflected, compare_to):
    if type_ == "table":
        # object.schema lấy giá trị từ __table_args__ = {"schema": "master"}
        return object.schema == "master"
    return True


def include_object_tenant(object, name, type_, reflected, compare_to):
    if type_ == "table":
        return object.schema is None
    return True


def get_tenants(connection):
    try:
        result = connection.execute(text("SELECT scheme FROM master.tenant"))
        return [f"tenant_{row[0]}" for row in result]
    except Exception as e:
        return []


# --- 4. Migration Execution ---


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_object=include_object_master,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        # ============================================
        # PHASE 1: MIGRATE MASTER SCHEMA
        # ============================================
        print("🚀 [Alembic] Migrating Schema: MASTER")

        connection.execute(text("CREATE SCHEMA IF NOT EXISTS master"))
        connection.execute(text("SET search_path TO master, public"))
        connection.commit()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object_master,
            version_table_schema="master",
        )

        with context.begin_transaction():
            context.run_migrations()

        # ============================================
        # PHASE 2: MIGRATE DYNAMIC TENANTS
        # ============================================
        tenants = get_tenants(connection)

        for tenant_schema in tenants:
            print(f"🚀 [Alembic] Migrating Schema: {tenant_schema}")

            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant_schema}"))
            connection.execute(text(f"SET search_path TO {tenant_schema}, public"))
            connection.commit()

            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                include_schemas=True,
                include_object=include_object_tenant,
                version_table_schema=tenant_schema,
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
