# api/v1/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.model import ModelCreate
from services.model import ModelService
from deps.deps import get_db_session, get_current_payload
from utils.hash import get_password_hash
from models.user import User 

router = APIRouter(
    prefix="/api/v1/model",
    tags=["模型管理"]
)


@router.post("/add", summary="添加模型")
async def add_model(config_data: ModelCreate, 
                    payload: dict = Depends(get_current_payload),
                    db_session: AsyncSession = Depends(get_db_session)):

    user_id = payload["id"]
    model = await ModelService.get_model_by_name(db_session, user_id, config_data.model_name)
    if model:
        raise HTTPException(status_code=409, detail="模型名已存在")
    
    try:
        new_model = await ModelService.create_model(
            db_session,
            user_id,
            config_data.model_name,
            config_data.url,
            config_data.api_key,
            config_data.model_type,
            config_data.summary
        )
    except Exception as e:
        # await db_session.rollback()
        print(f"错了？{e}")
        raise HTTPException(500, detail="服务器内部错误,模型创建失败")
    
    return {"message":"添加模型成功", "model.id": new_model.id}


@router.get("/all", summary="获取该用户的所有模型")
async def get_all(payload: dict = Depends(get_current_payload),db_session: AsyncSession = Depends(get_db_session)):
    user_id = payload["id"]

    try:
        models = await ModelService.get_models(db_session, user_id)
        response = {
            "message": "获取模型列表成功",
            "models": models
        }
        return response
    except Exception as e:
        print(f"获取模型列表错误: {e}")
        raise HTTPException(
            status_code=500, 
            detail="服务器内部错误，获取模型列表失败"
        )
    
@router.delete("/delete", summary="删除该用户的某个模型")
async def delete_model(
        model_name: str,
        payload: dict = Depends(get_current_payload),
        db_session: AsyncSession = Depends(get_db_session)
    ):
    user_id = payload["id"]
    try:
        model = await ModelService.get_model_by_name(db_session, user_id, model_name)
        if model is None:
            raise HTTPException(404, detail=f"该模型{model_name}不存在")

        res = await ModelService.delete_model(db_session, user_id, model_name)
        if res:
            return {"message":"删除成功!"}
        else:
            return {"message":"删除失败"}

    except Exception as e:
        print(f"删除模型错误: {e}")
        raise HTTPException(
            status_code=500, 
            detail="服务器内部错误，删除模型列表失败"
        )