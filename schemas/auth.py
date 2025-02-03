from pydantic import BaseModel


class UserCreateResponse(BaseModel):
    id: int
    email: str


class TokenInfo(BaseModel):
    access_token: str
