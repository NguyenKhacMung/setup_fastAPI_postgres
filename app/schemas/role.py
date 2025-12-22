import uuid
from pydantic import BaseModel
from typing import List


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase): ...


class RoleRead(RoleBase):
    id: uuid.UUID
    permissions: List[str] = []


class RoleUpdate(RoleBase):
    permissions: List[str] = []
