from sqlmodel import Field, SQLModel


class Permission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str
