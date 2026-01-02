from sqlmodel import Field

from app.models.master.base import MasterBase


class Role(MasterBase, table=True):
    __tablename__ = "role"

    id: int | None = Field(default=None, primary_key=True)
    role_name: str
