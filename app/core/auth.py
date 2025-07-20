from datetime import datetime, timedelta
from typing import Any, Optional
import logging

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = settings.ALGORYTHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return True

def get_password_hash(password: str) -> Any:
    logger.info("Hashing password")
    return pwd_context.hash(password)

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
    ) -> str:
    return "pass"

def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None) -> str:
    return "pass"

def decode_token(token: str) -> Optional[dict]:
    pass