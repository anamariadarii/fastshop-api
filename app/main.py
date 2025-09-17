from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ importă router-ele
from .routers import users, products

app = FastAPI(title="FastShop API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

# ✅ montează router-ele
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
