# /models/model.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum  #  标准库的 Enum
from sqlalchemy import Enum as SqlEnum  #  SQLAlchemy 的 Enum（避免命名冲突）

from db.database import Base



# 定义LLM类型枚举
class ModelType(str, Enum):
    LLM = "llm"
    EMBEDDING = "embedding"
    RERANK = "rerank"


class Model(Base):
    __tablename__ = "models"
    # 防止不同用户使用相同模型名而冲突, 建立联合索引
    __table_args__ = (UniqueConstraint("user_id", "model_name", name="uq_user_modelname"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    model_name = Column(String(100), nullable=False)  # 模型名称
    url = Column(String(255), nullable=False)  # 模型接口地址
    api_key = Column(String(255), nullable=False)  # API密钥
    model_type = Column(SqlEnum(ModelType), nullable=False)
    summary = Column(String(255), default="")  # 模型说明
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联用户
    user = relationship("User", back_populates="model")