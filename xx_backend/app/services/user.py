# services/auth_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from models.user import User

class UserService:
    @staticmethod
    async def get_user_by_email(async_session: AsyncSession, email: str) -> User | None:
        result = await async_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
        # return result.scalars().first()

    @staticmethod
    async def get_user_by_username(async_session: AsyncSession, username: str) -> User | None:
        result = await async_session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(async_session: AsyncSession) -> list[User]:
        result = await async_session.execute(select(User).order_by(User.id))
        return result.scalars().all()
        # return result.scalars().fetchall()

    @staticmethod
    async def create_user(async_session: AsyncSession, username: str, password_hashed: str, email: str) -> User:
        user = User(username=username, password_hashed=password_hashed, email=email)
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)
        return user

    @staticmethod
    async def update_user(async_session: AsyncSession, user_id: int, **kwargs) -> bool:
        response = update(User).where(User.id == user_id)
        result = await async_session.execute(response.values(**kwargs))
        await async_session.commit()
        return result.rowcount > 0

    @staticmethod
    async def delete_user(async_session: AsyncSession, user_id: int) -> bool:
        response = await async_session.execute(delete(User).where(User.id == user_id))
        await async_session.commit()
        return response.rowcount > 0