from typing import ClassVar
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from app.models import Role, RolePermission


class PermissionBase(SQLModel):
    code: str


class Permission(PermissionBase, table=True):
    __tablename__: ClassVar[str] = "permissions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )
