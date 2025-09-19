from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import Dict, List
import os, time, jwt

router = APIRouter(tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv(
    "JWT_SECRET",
    "0f8c2e3a9d674fc98c3f4a7a2d93b6711c0e1b6f5a824c9bb23f0c7d9e2f5b61",
)
ALGORITHM = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

_users: List[Dict[str, object]] = []

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str) -> str:
    now = int(time.time())
    exp = now + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = {"sub": subject, "iat": now, "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    if any(u["email"] == user.email for u in _users):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = {
        "id": len(_users) + 1,
        "email": user.email,
        "password": get_password_hash(user.password),
    }
    _users.append(new_user)
    return {"id": new_user["id"], "email": new_user["email"]}

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = next((u for u in _users if u["email"] == user.email), None)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
