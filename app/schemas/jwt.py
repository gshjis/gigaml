from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JWTToken(BaseModel):
    sub: str  # Subject (e.g., user ID) - Identifies the subject of the token, typically the user ID.
    exp: Optional[int] = None  # Expiration time (UNIX timestamp) - Specifies when the token expires.
    iat: Optional[int] = None  # Issued at time (UNIX timestamp) - Indicates when the token was issued.
    nbf: Optional[int] = None  # Not before time (UNIX timestamp) - Specifies when the token is valid from.
    aud: Optional[str] = None  # Audience - Identifies the intended audience of the token.
    iss: Optional[str] = None  # Issuer - Identifies the issuer of the token.
    jti: Optional[str] = None  # JWT ID - Unique identifier for the token.

    class Config:
        from_attributes = True

    @classmethod
    def from_token(cls, token: str) -> 'JWTToken':
        # Placeholder for decoding a JWT token into this schema
        # This would typically use a library like `pyjwt` to decode the token
        return cls(sub="dummy_sub", exp=int(datetime.utcnow().timestamp()) + 3600)

class RefreshToken(BaseModel):
    sub: str  # Subject (e.g., user ID) - Identifies the subject of the token, typically the user ID.
    jti: str  # JWT ID - Unique identifier for the token.
    exp: int  # Expiration time (UNIX timestamp) - Specifies when the token expires.
    iat: int  # Issued at time (UNIX timestamp) - Indicates when the token was issued.

    class Config:
        from_attributes = True

    @classmethod
    def create(cls, sub: str, expiration_minutes: int = 1440) -> 'RefreshToken':
        now = int(datetime.utcnow().timestamp())
        return cls(
            sub=sub,
            jti=str(uuid.uuid4()),  # Generate a unique JWT ID
            exp=now + expiration_minutes * 60,
            iat=now,
        )

    @classmethod
    def from_token(cls, token: str) -> 'RefreshToken':
        # Placeholder for decoding a refresh token into this schema
        # This would typically use a library like `pyjwt` to decode the token
        return cls(sub="dummy_sub", jti="dummy_jti", exp=int(datetime.utcnow().timestamp()) + 3600)
