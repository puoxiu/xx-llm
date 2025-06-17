from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text


from core.config import settings
from db.database import async_engine, Base
from api import user, model


# 生命周期管理器
# 仅在开发环境推荐使用
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时
    async with async_engine.begin() as conn:
        # 遍历所有继承自 Base 的 ORM 模型类，根据模型定义在数据库中创建对应的表结构
        await conn.run_sync(Base.metadata.create_all)
        try:
            await conn.execute(text("SELECT 1"))
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            # 可选：在连接失败时阻止应用启动
            raise
    
    yield  # 应用运行时
    
    # 应用关闭时
    if isinstance(async_engine, AsyncEngine):
        await async_engine.dispose()
        print("数据库连接池已关闭")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(user.router)
app.include_router(model.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )