# /schemas/model.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from enum import Enum



# 定义与数据库一致的模型类型枚举
class ModelTypeEnum(str, Enum):
    LLM = "llm"
    EMBEDDING = "embedding"
    RERANK = "rerank"

class ModelCreate(BaseModel):
    model_name: str = Field(..., max_length=100, description="模型名称")
    url: Optional[str] = Field(..., max_length=255, description="API基础URL")
    api_key: Optional[str] = Field(..., max_length=255, description="API密钥")
    model_type: ModelTypeEnum = Field(..., description="模型类型，可选: llm, embedding, rerank")
    summary: str = Field(...,max_length=255, description="模型说明")

    # 可选：添加验证器确保输入合法性
    @field_validator("model_type")
    def validate_model_type(cls, v):
        if v not in [mt.value for mt in ModelTypeEnum]:
            raise ValueError("无效的模型类型")
        return v
    
