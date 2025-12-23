from uuid import uuid4, UUID
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str

    role_id: UUID | None = Field(default=None, foreign_key="roles.id")
    role: Optional["Role"] = Relationship(back_populates="users")
