from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str]
    namespace: str
    llm_config: dict

    class Config:
        orm_mode = True
