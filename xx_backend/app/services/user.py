# services/auth_service.py
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth import JWTUtils
from sqlalchemy import select, update, delete

from utils.hash import verify_password, get_password_hash
from utils.namespace import generate_namespace  # 自动生成唯一命名空间


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
    async def update_user(async_session: AsyncSession, user_id: int, **kwargs):
        response = update(User).where(User.id == user_id)
        result = await async_session.execute(response.values(**kwargs))
        await async_session.commit()
        return result

    @staticmethod
    async def delete_user(async_session: AsyncSession, user_id: int):
        response = await async_session.execute(delete(User).where(User.id == user_id))
        await async_session.commit()
        return response

    @staticmethod
    async def check_user_phone_email_and_password(async_session: AsyncSession, email: str, password_hashed: str) -> User | None:
        result = await async_session.execute(select(User).where(User.email == email and User.password_hashed == password_hashed))
        user = result.scalar_one_or_none()
        return user


def register_user(db: AsyncSession, user_data):
    if db.query(User).filter_by(email=user_data.email).first():
        raise ValueError("Email exists")
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        namespace=generate_namespace()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: AsyncSession, email: str, password: str):
    user = db.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    token = JWTUtils.token_encode({"sub": str(user.id)})
    return token, user
