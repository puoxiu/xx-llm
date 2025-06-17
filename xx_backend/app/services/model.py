# services/model.py
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update, delete

from models.model import Model, ModelType


class ModelService:
    @staticmethod
    async def get_models(async_session: AsyncSession, user_id: int) -> list[Model]:
        result = await async_session.execute(select(Model).where(Model.user_id == user_id))
        return result.scalars().all()
        # return result.scalars().first()
    
    # 根据模型名 查询某用户的某个模型是否存在
    @staticmethod
    async def get_model_by_name(async_session: AsyncSession, user_id: int, model_name: str) -> Model | None:
        result = await async_session.execute(select(Model).where(Model.user_id == user_id, Model.model_name == model_name))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_model(async_session: AsyncSession, 
                           user_id: int, model_name: str, url: str, api_key: str, model_type: ModelType, summary: str = ""
                        ) -> Model:
        model = Model(
            user_id=user_id, 
            model_name=model_name, 
            url=url,
            api_key=api_key, 
            model_type=model_type,
            summary=summary
        )
        async_session.add(model)
        await async_session.commit()
        await async_session.refresh(model)  # 获取自增 ID 等
        return model

    @staticmethod
    async def update_model(async_session: AsyncSession, model_name: str, **kwargs):
        response = update(Model).where(Model.model_name == model_name)
        result = await async_session.execute(response.values(**kwargs))
        await async_session.commit()
        return result.rowcount > 0


    @staticmethod
    async def delete_model(async_session: AsyncSession,user_id: int, model_name: str):
        response = await async_session.execute(delete(Model).where(Model.user_id == user_id, Model.model_name == model_name))
        await async_session.commit()
        return response.rowcount > 0
