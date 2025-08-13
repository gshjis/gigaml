from pydantic import BaseModel

from app.schemas.user import UserOut


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(TokenResponse):
    user: UserOut
