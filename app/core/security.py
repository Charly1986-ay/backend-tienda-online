from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return password_hash.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALG
    )
    return encoded_jwt

def decode_token(token: str) -> dict:
    payload = jwt.decode(
        jwt=token, 
        key=settings.JWT_SECRET, 
        algorithms=[settings.JWT_ALG]
    )
    return payload