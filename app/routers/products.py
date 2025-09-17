from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductOut(ProductCreate):
    id: int

_memory = []  # demo in-memory

@router.post("", response_model=ProductOut)
async def create_product(p: ProductCreate):
    item = {"id": len(_memory) + 1, **p.model_dump()}
    _memory.append(item)
    return item

@router.get("", response_model=List[ProductOut])
async def list_products():
    return _memory
