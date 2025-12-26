from typing import ClassVar
from uuid import UUID
from sqlmodel import SQLModel, Field


class RolePermission(SQLModel, table=True):
    __tablename__: ClassVar[str] = "role_permissions"

    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="permissions.id", primary_key=True)
