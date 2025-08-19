from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.dev"),  # 按照顺序读取
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = ""
    MYSQL_PORT: str = ""
    MYSQL_DB: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    REDIS_HOST: str = ""
    REDIS_PORT: str = ""
    REDIS_PASSWORD: str = ""


settings = Settings()
