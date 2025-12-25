from pydantic import BaseModel
from sqlmodel import Field
from app.models.user import UserBase


class LoginBody(UserBase):
    password: str = Field(min_length=8, max_length=12)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int
    exp: int
