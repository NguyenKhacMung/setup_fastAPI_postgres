from sqlmodel import SQLModel, Field, Relationship
from app.models.role import Role


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role_id: int | None = Field(foreign_key="role.id")
    role: Role | None = Relationship()
