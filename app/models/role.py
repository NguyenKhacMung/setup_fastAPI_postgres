from __future__ import annotations
import uuid
from typing import List
from sqlmodel import SQLModel, Field, Relationship
from app.models.permission import Permission


class RolePermission(SQLModel, table=True):
    role_id: uuid.UUID = Field(foreign_key="role.id", primary_key=True)
    permission_id: uuid.UUID = Field(foreign_key="permission.id", primary_key=True)


class Role(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="role")  # forward reference
    permissions: List[Permission] = Relationship(link_model=RolePermission)
