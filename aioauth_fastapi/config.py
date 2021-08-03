from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AIOAuth FastAPI example"
    PROJECT_HOST: str = "0.0.0.0"
    PROJECT_PORT: int = 8001
    DEBUG: bool = False

    REDIS_DSN: str
    PSQL_DSN: str

    JWT_PUBLIC_KEY: str = ""
    JWT_PRIVATE_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
