from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 用户修改密码
class UserUpdata(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
    # re_new_password: str

class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str]
    namespace: str
    llm_config: dict

    # class Config:
    #     orm_mode = True
    
    class Config:
        from_attributes = True  # V2写法
