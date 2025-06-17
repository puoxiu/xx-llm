# deps.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


from models.user import User
from db.database import async_session
from core.config import settings
from core.auth import AuthTokenHelper
from services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login1")

# 依赖注入 + 自动资源管理的结合
# 依赖注入：函数的参数是其他函数的返回值，这种方式称为依赖注入
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_session = None
    try:
        db_session = async_session()
        yield db_session
    finally:
        await db_session.close()


async def get_current_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = AuthTokenHelper.token_decode(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return payload


