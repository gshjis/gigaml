import logging
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core.exceptions import InvalidTokenException
from app.core.settings import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check password`s matching to it`s hash

    Args:
        plain_password (str): _description_
        hashed_password (str): _description_

    Returns:
        bool: _description_
    """
    status = pwd_context.verify(plain_password, hashed_password)
    return status


def get_password_hash(password: str) -> str:
    """Get password hash

    Args:
        password (str): user`s password

    Returns:
        str: password`s hash
    """
    return pwd_context.hash(password)


def from_token(token: str, secret_key: str, algorithms: str) -> Dict[str, str]:
    """Token decoder

    Args:
        token (str): JWT access toke
        secret_key (str): secrete key
        algorithms (list[str]): decode algorythm

    Returns:
        Dict: model of access token

    Raises:
        InvalidTokenException: If the token is invalid or expired
    """
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithms)
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenException("Invalid token")


def create_jwt(
    data: Dict[str, Any],
    algorithm: str,
    secret_key: str,
    exp_timedelta: timedelta,
) -> str:
    payload = data.copy()
    expiration = datetime.now() + exp_timedelta
    payload["exp"] = int(expiration.timestamp())

    return jwt.encode(payload, secret_key, algorithm=algorithm)
