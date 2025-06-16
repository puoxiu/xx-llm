from pydantic import BaseModel, Field
from typing import Optional, Dict, Any



class ModelCreate(BaseModel):
    model_name: str = Field(..., max_length=100, description="模型名称")
    url: Optional[str] = Field(..., max_length=255, description="API基础URL")
    api_key: Optional[str] = Field(..., max_length=255, description="API密钥")
    model_type: int = Field(..., description="模型类型")
    parameters: Dict[str, Any] = Field(default={}, description="模型参数")

