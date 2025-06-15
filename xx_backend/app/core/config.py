from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # app
    APP_NAME: str = "xingxing-LLM助手平台"
    APP_VERSION: str = "1.0.0"
    
    # 数据库-MySQL
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_HOST: str = "182.61.13.121"
    DB_PORT: int = 3306
    DB_NAME: str = "xingxing_llm"
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # jwt
    SECRET_KEY: str = "xingxing_auth"
    ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 120

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()