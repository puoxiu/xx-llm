# api/v1/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserLogin, UserInDB, UserUpdata
from services.user import UserService
from deps.deps import get_db_session
from utils.hash import get_password_hash, verify_password
from core.auth import AuthTokenHelper

router = APIRouter(
    prefix="/api/v1/user",
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
    # 返回注册成功信息
    return {"msg": "注册成功", "redirect_url": "/api/v1/user/login"}


@router.post("/login1", summary="登录接口1-接收表单数据用于测试")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_db_session)):
    # 注意：OAuth2PasswordRequestForm 中的字段是 username 而不是 email！
    user = await UserService.get_user_by_email(db_session, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="email 或密码错误1")
    
    if not verify_password(form_data.password, user.password_hashed):
        raise HTTPException(status_code=400, detail="email 或密码错误2")

    payload = {
        'sub': 'xingxing',
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'scopes': ["user"],  # 可选
    }
    token = AuthTokenHelper.token_encode(payload)

    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/login", summary="登录接口")
async def login(login_data: UserLogin, db_session: AsyncSession = Depends(get_db_session)):
    user = await UserService.get_user_by_email(db_session, login_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email或密码错误1")

    if not verify_password(login_data.password, user.password_hashed):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email或密码错误2")
    
    payload = {
        'sub': 'xingxing',
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'admin': True,
    }
    token = AuthTokenHelper.token_encode(payload)

    return {'msg': '登录成功!', 'access_token': token, 'token_type': 'bearer'}

@router.put("/update_pwd", summary="修改密码")
async def update_pwd(update_data: UserUpdata, db_session: AsyncSession = Depends(get_db_session)):
    user = await UserService.get_user_by_email(db_session, update_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email或密码错误")
    if not verify_password(update_data.old_password, user.password_hashed):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email或密码错误2")

    # 更新
    new_password_hashed = get_password_hash(update_data.new_password)
    update_success = await UserService.update_user(
        db_session,
        user_id=user.id,
        password_hashed=new_password_hashed
    )
    if not update_success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="密码更新失败")
    
    return {"message":"密码更新成功"}