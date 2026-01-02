from sqlmodel import Field

from app.models.tenant.base import TenantBase


class TenantUser(TenantBase, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    username: str | None = None
    system_role: str
    password_hash: str | None = None
