from app.settings import ALGORITHM, SECRET_KEY, oauth2_scheme, pwd_context

DATABASE_URL = "sqlite:///:memory:"

pwd_context = pwd_context

# JWT Token
SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 10

# OAuth 2.0
oauth2_scheme = oauth2_scheme

