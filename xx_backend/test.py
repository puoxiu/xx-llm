from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

async def test_connection():
    engine = create_async_engine(settings.ASYNC_DATABASE_URL)
    async with engine.connect() as conn:
        result = await conn.execute("SELECT 1")
        print("连接成功，结果:", result.scalar())
    await engine.dispose()

asyncio.run(test_connection())