import os
import time
from typing import Optional

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET: str = os.getenv(
    "JWT_SECRET",
    "0f8c2e3a9d674fc98c3f4a7a2d93b6711c0e1b6f5a824c9bb23f0c7d9e2f5b61",
)
JWT_ALG: str = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRES_MIN: int = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", "60"))


def hash_password(password: str) -> str:
    return _pwd_ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_ctx.verify(plain_password, hashed_password)


def make_token(user_id: int, expires_in_minutes: Optional[int] = None) -> str:
    minutes = expires_in_minutes or ACCESS_TOKEN_EXPIRES_MIN
    now = int(time.time())
    payload = {"sub": user_id, "iat": now, "exp": now + 60 * minutes}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token: str) -> int:
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        if "sub" not in data:
            raise ValueError("Token fără 'sub'")
        return int(data["sub"])
    except ExpiredSignatureError:
        raise ValueError("Token expirat")
    except InvalidTokenError:
        raise ValueError("Token invalid")


async def get_current_user_id(authorization: str = Header(...)) -> int:
    prefix = "Bearer "
    if not authorization or not authorization.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Lipsește Bearer token"
        )
    token = authorization[len(prefix) :].strip()
    try:
        return decode_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )
