from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from app.models.role_permission import RolePermission


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str

    users: list["User"] = Relationship(back_populates="role")

    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
