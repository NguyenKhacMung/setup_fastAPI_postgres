from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.role_permission import RolePermission

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.permission import Permission


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str

    users: list["User"] = Relationship(back_populates="role")

    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
