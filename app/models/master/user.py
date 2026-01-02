from sqlmodel import Field

from app.models.master.base import MasterBase


class PlatformUser(MasterBase, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    system_role: str
