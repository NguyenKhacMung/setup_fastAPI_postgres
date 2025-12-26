from uuid import UUID, uuid4
from typing import TYPE_CHECKING, ClassVar
from sqlmodel import SQLModel, Field, Relationship
from app.models.role_permission import RolePermission

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.permission import Permission


class RoleBase(SQLModel):
    name: str


class Role(RoleBase, table=True):
    __tablename__: ClassVar[str] = "roles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    users: list["User"] = Relationship(back_populates="role")

    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
