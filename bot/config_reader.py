from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Config class."""

    BOT_TOKEN: str
    ANON_ADMIN_ID: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
