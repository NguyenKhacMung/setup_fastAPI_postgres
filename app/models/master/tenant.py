from sqlmodel import Field
from uuid import UUID

from app.models.master.base import MasterBase


class Tenant(MasterBase, table=True):
    __tablename__ = "tenant"

    id: UUID = Field(primary_key=True)
    name: str
    scheme: str
    business_model: str | None = None
