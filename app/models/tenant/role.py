from sqlmodel import Field

from app.models.tenant.base import TenantBase


class TenantRole(TenantBase, table=True):
    __tablename__ = "tenant_role"

    id: int | None = Field(default=None, primary_key=True)
    role_name: str
