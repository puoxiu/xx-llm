# deps.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


from models.user import User
from db.database import async_session
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(async_session)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# 依赖注入 + 自动资源管理的结合
# 依赖注入：函数的参数是其他函数的返回值，这种方式称为依赖注入
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_session = None
    try:
        db_session = async_session()
        yield db_session
    finally:
        await db_session.close()