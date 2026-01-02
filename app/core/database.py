from typing import Annotated
from sqlalchemy import text
from sqlmodel import create_engine, Session
from fastapi import Depends
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


# def get_session(schema: str):
#     with Session(engine) as session:
#         session.exec(text(f'SET search_path TO "{schema}", public'))
#         yield session


SessionDep = Annotated[Session, Depends(get_session)]
