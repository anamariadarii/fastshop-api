import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test_connection():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:admin@localhost:5432/fastshop", echo=True
    )
    try:
        async with engine.begin() as conn:
            print("✅ Conexiune OK la PostgreSQL!")
    except Exception as e:
        print("❌ Eroare conexiune:", e)

asyncio.run(test_connection())
