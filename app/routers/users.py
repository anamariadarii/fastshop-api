from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    # demo: întoarce un user dummy
    return {"id": 1, "email": user.email}

@router.post("/login")
async def login(user: UserCreate):
    return {"access_token": "demo", "token_type": "bearer"}
