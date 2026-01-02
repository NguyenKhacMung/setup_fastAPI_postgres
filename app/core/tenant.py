from contextvars import ContextVar

_current_schema = ContextVar("current_schema", default="master")


def set_schema(schema: str):
    _current_schema.set(schema)


def get_schema() -> str:
    return _current_schema.get()
