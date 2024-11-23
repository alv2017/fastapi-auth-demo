from datetime import UTC, datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.operations import get_user
from app.db.schema import User as db_User
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class InvalidTokenError(Exception):
    default_message = "Invalid token"

    def __init__(self, message=default_message):
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(Exception):
    default_message = "Token expired"

    def __init__(self, message=default_message):
        self.message = message
        super().__init__(self.message)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    if "exp" not in to_encode:
        token_expiration_time = datetime.now(tz=UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.timestamp(token_expiration_time)
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str, session: Session) -> Optional[db_User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        return
    if not username:
        return
    user: Optional[db_User] = get_user(session, username)
    return user
