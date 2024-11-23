from typing import Optional

from email_validator import EmailNotValidError, validate_email
from sqlalchemy.orm import Session

from app.db.schema import User as db_User
from app.settings import pwd_context


def authenticate_user(session: Session, username_or_email: str, password: str) -> Optional[db_User]:
    try:
        validate_email(username_or_email)
        query_filter = db_User.email
    except EmailNotValidError:
        query_filter = db_User.username

    user: Optional[db_User] = session.query(db_User).filter(query_filter == username_or_email).first()

    if not user or not pwd_context.verify(password, user.hashed_password):
        return

    return user
