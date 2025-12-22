from sqlmodel import SQLModel, Field, Relationship
from app.models.permission import Permission


class RolePermission(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    permissions: list[Permission] = Relationship(link_model=RolePermission)
