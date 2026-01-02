from typing import Annotated
from sqlalchemy import text
from sqlmodel import create_engine, Session
from fastapi import Depends
from app.core.config import settings
from app.core.tenant import get_schema

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)


def get_session():
    with Session(engine) as session:
        schema = get_schema()
        session.exec(text(f'SET search_path TO "{schema}"'))
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
