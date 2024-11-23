from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./db.sqlite"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Token
SECRET_KEY = "secret-key-123123000"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth 2.0
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Logging
LOG_FILE_LOCATION = "/var/applications/fastapi-auth-demo/logs/client.log"
ENABLE_CLIENT_LOGGING = False
