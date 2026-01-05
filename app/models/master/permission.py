from sqlmodel import Field

from app.models.master.base import MasterBase


class PlatformPermission(MasterBase, table=True):
    __tablename__ = "permission"

    id: int | None = Field(default=None, primary_key=True)
    permission_name: str
