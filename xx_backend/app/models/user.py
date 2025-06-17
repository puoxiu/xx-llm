# models/user.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
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

    # 关联模型配置表
    model = relationship("Model", back_populates="user", cascade="all, delete-orphan")
