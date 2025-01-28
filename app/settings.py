from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str

    # JWT Token
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_FILE_LOCATION: str
    ENABLE_CLIENT_LOGGING: bool

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore[call-arg]

# Hashing
pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth 2.0
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/token")
