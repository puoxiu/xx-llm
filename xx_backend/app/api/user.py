# api/v1/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserLogin, UserInDB
from services.user import UserService
from deps.deps import get_db_session
from utils.hash import get_password_hash
from core.auth import AuthTokenHelper

router = APIRouter(
    prefix="/app/v1/user",
    tags=["用户管理"]
)

# @router.post("/register", summary="注册接口", response_model=UserInDB)
@router.post("/register", summary="注册接口")
async def register(register_data: UserCreate, db_session: AsyncSession = Depends(get_db_session)):
    user = await UserService.get_user_by_username(db_session, register_data.username)
    # 检查用户名和手机号是否已存在
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或手机号已存在")
    
    password_hashed = get_password_hash(register_data.password)
    await UserService.create_user(db_session, register_data.username, password_hashed, register_data.email)
    # 返回注册成功信息, 并且重定向到登录页面
    return {"msg": "注册成功", "redirect_url": "/api/v1/user/login"}

@router.post("/login", summary="登录接口")
async def login(login_data: UserLogin, db_session: AsyncSession = Depends(get_db_session)):
    password_hashed = get_password_hash(login_data.password)
    user = await UserService.check_user_phone_email_and_password(db_session, login_data.email, password_hashed)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="手机号或密码错误")
    
    payload = {
        'sub': 'xingxing',
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'admin': True,
    }
    token = AuthTokenHelper.token_encode(payload)

    return {'msg': '登录成功!', 'access_token': token, 'token_type': 'bearer'}
