# api/v1/user.py
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.model import ModelCreate
from services.user import UserService

from deps.deps import get_db_session, get_current_user
from utils.hash import get_password_hash
from core.auth import AuthTokenHelper
from models.user import User 

router = APIRouter(
    prefix="/app/v1/model",
    tags=["用户管理"]
)



@router.post("/add", summary="添加模型")
async def add_model(config_data: ModelCreate, 
                    current_user: User = Security(get_current_user, scopes=["user"]),
                    db_session: AsyncSession = Depends(get_db_session)):
    pass
    