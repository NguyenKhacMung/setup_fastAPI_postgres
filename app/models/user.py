import uuid
from sqlmodel import SQLModel, Field, Relationship
from app.models.role import Role


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    role_id: uuid.UUID | None = Field(default=None, foreign_key="role.id")
    role: Role | None = Relationship(back_populates="users")
