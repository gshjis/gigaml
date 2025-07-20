from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TokenPayload(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
