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
 
    @staticmethod
    async def create_model(async_session: AsyncSession, 
                           user_id: int, model_name: str, url: str, api_key: str, model_type: ModelType) -> Model:
        model = Model(user_id=user_id, model_name=model_name, url=url, api_key=api_key, model_type=model_type)
        async_session.add(model)
        await async_session.commit()
        await async_session.refresh(model)
        return model

    @staticmethod
    async def update_model(async_session: AsyncSession, model_name: str, **kwargs):
        response = update(Model).where(Model.model_name == model_name)
        result = await async_session.execute(response.values(**kwargs))
        await async_session.commit()
        return result.rowcount > 0


    @staticmethod
    async def delete_model(async_session: AsyncSession, model_name: str):
        response = await async_session.execute(delete(Model).where(Model.model_name == model_name))
        await async_session.commit()
        return response.rowcount > 0
