# models/user.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hashed = Column(String(128), nullable=False)
    avatar = Column(String(255), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    # 用户自定义的模型访问配置（如OpenAI、DeepSeek等）
    llm_config = Column(JSON, default={})  # {provider: "openai", api_key: "...", base_url: "..."}

    # 多租户命名空间
    namespace = Column(String(64), unique=True)
