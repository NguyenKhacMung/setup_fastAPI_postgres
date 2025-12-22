import uuid
from sqlmodel import SQLModel, Field


class Permission(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    code: str
