from typing import Annotated
from fastapi import APIRouter, Header
from sqlalchemy import text

from app.core.database import SessionDep
from app.core.tenant import schema_ctx

from app.schemas.auth import LoginRequest


router = APIRouter(tags=["Login"])


@router.post(
    "/login",
)
def login(
    db: SessionDep,
    _: Annotated[str | None, Header(alias="X-TENANT-ID")] = None,
):
    print("before:", db.exec(text("SELECT current_schema()")).one())

    with schema_ctx(db, "ccc"):
        print("inside:", db.exec(text("SELECT current_schema()")).one())

    print("after:", db.exec(text("SELECT current_schema()")).one())

    return {"permissions": "ccc"}
