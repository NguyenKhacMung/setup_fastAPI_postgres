from contextlib import contextmanager
from contextvars import ContextVar

from sqlalchemy import text
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
    prev = session.exec(text("SHOW search_path")).one()[0]
    session.exec(text(f'SET search_path TO "{schema}"'))
    try:
        yield
    finally:
        session.exec(text(f"SET search_path TO {prev}"))
