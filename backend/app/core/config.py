from pydantic_settings import BaseSettings
from pydantic import Field



class Settings(BaseSettings):
    app_name: str = Field(..., env="APP_NAME")
    environment : str = Field(..., env="ENVIRONMENT")



    database_url: str = Field(..., env="DATABASE_URL")
    test_database_url: str = Field(..., env="TEST_DATABASE_URL")

    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(..., env="JWT_ALGORITHM")
    jwt_expiration: int = Field(..., env="JWT_EXPIRATION")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()