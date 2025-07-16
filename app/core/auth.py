from datetime import datetime, timedelta
from typing import Optional
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
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    logger.info("Verifying password")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    logger.info("Hashing password")
    return pwd_context.hash(password)

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None) -> str:
    logger.info("Creating access token")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"sub": str(data["sub"]), "exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None) -> str:
    logger.info("Creating refresh token")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"sub": data["sub"], "exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    logger.info("Decoding token")
    try:
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload if payload else None
    except JWTError as e:
        logger.error(f"Token decoding error: {str(e)}")
        return None
