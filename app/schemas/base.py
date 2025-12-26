from pydantic import BaseModel, Field
from typing import Literal


class PagingRequest(BaseModel):
    search: str | None = None
    filter: dict[str, str] | None = None

    sort_by: str | None = None
    sort_order: Literal["asc", "desc"] = "asc"

    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
