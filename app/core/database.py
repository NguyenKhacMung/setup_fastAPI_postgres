from typing import Annotated
from sqlmodel import create_engine, Session
from fastapi import Depends, Header
from app.core.config import settings
from app.core.tenant import get_schema

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)


# def get_session():
#     with Session(engine) as session:
#         schema = get_schema()
#         session.exec(text(f'SET search_path TO "{schema}"'))
#         yield session


DEFAULT_SCHEMA = "master"


def get_tenant_schema(
    tenant_id: Annotated[str | None, Header(alias="X-TENANT-ID")] = None,
) -> str:
    return tenant_id or DEFAULT_SCHEMA


def get_session(schema: str = Depends(get_tenant_schema)):
    with Session(engine) as session:
        session.connection().exec_driver_sql(f'SET search_path TO "{schema}"')
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
