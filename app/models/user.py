from datetime import datetime
from typing import ClassVar
from uuid import uuid4, UUID
from sqlmodel import Column, SQLModel, Field, Relationship, func, DateTime
from app.models.role import Role


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    __tablename__: ClassVar[str] = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )

    role_id: UUID | None = Field(
        default=None, foreign_key="roles.id", ondelete="SET NULL"
    )
    role: Role | None = Relationship(back_populates="users")
