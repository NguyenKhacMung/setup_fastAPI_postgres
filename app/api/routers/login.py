from fastapi import APIRouter
from sqlalchemy import func
from sqlmodel import select

from app.core.database import SessionDep
from app.core.tenant import schema_ctx

from app.models.master.tenant import Tenant
from app.models.tenant.user import TenantUser


router = APIRouter(tags=["Login"])


@router.post(
    "/login",
)
def login(db: SessionDep):
    print("before:", db.exec(select(func.current_schema())).one())
    # tenant = db.exec(select(Tenant)).all()
    # print("tenant", tenant)
    # tenant_user = db.exec(select(TenantUser)).all()
    # print("tenant_user", tenant_user)

    with schema_ctx(db, "tenant_001"):
        print("inside:", db.exec(select(func.current_schema())).one())

    print("after:", db.exec(select(func.current_schema())).one())

    return {"permissions": "ccc"}
