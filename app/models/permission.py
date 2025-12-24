from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from app.models.role_permission import RolePermission
from app.models.role import Role


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    code: str

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )
