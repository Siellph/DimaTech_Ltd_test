from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    JWT_SECRET_SALT: str


settings = Settings()
