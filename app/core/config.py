from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'AutoGrader B-4 基础服务'
    VERSION: str = '0.1.0'
    API_V1_PREFIX: str = '/api/v1'

    DATABASE_URL: str = 'sqlite:///./autograder_b4.db'
    SECRET_KEY: str = 'change-me-in-production'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
