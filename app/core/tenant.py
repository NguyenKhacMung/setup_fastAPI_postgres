from contextlib import contextmanager
from contextvars import ContextVar

from sqlmodel import Session

# ========= ContextVar =========
_current_schema = ContextVar("current_schema", default="master")


def set_schema(schema: str):
    _current_schema.set(schema)


def get_schema() -> str:
    return _current_schema.get()


# ========= DB schema switch =========
@contextmanager
def schema_ctx(session: Session, schema: str):
    conn = session.connection()

    prev = conn.exec_driver_sql("SHOW search_path").scalar_one()

    conn.exec_driver_sql(f'SET search_path TO "{schema}"')
    try:
        yield
    finally:
        conn.exec_driver_sql(f"SET search_path TO {prev}")
