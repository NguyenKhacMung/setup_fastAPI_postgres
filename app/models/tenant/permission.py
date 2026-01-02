from sqlmodel import Field

from app.models.tenant.base import TenantBase


class TenantPermission(TenantBase, table=True):
    __tablename__ = "tenant_permission"

    id: int | None = Field(default=None, primary_key=True)
    permission_name: str
