from sqlmodel import SQLModel
from sqlalchemy import MetaData


master_metadata = MetaData(schema="master")


class MasterBase(SQLModel):
    metadata = master_metadata
