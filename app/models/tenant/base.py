from sqlmodel import SQLModel
from sqlalchemy import MetaData


tenant_metadata = MetaData()


class TenantBase(SQLModel):
    metadata = tenant_metadata
