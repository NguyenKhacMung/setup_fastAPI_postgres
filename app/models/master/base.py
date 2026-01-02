from sqlmodel import SQLModel


class MasterBase(SQLModel):
    __table_args__ = {"schema": "master"}
