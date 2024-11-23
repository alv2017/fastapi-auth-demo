from typing import Optional, Type

from email_validator import EmailNotValidError, validate_email
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.settings import pwd_context

from .schema import Role
from .schema import User as db_User


class UserExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def add_user(session: Session, username: str, email: str, password: str, role: Role = Role.basic) -> Optional[db_User]:
    hashed_password = pwd_context.hash(password)
    db_user = db_User(username=username, email=email, hashed_password=hashed_password, role=role)
    session.add(db_user)
    try:
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        session.rollback()
        return
    return db_user


def get_user(session: Session, username_or_email: str) -> Optional[db_User]:
    try:
        validate_email(username_or_email)
        query_filter = db_User.email
    except EmailNotValidError:
        query_filter = db_User.username

    db_user: Optional[db_User] = session.query(db_User).filter(query_filter == username_or_email).first()
    return db_user


def get_all_users(session: Session) -> list[Type[db_User]]:
    return session.query(db_User).all()


def get_user_by_id(uid: int, session: Session) -> Optional[db_User]:
    return session.query(db_User).filter(db_User.id == uid).first()


def update_user_data(uid: int, update_data: dict, session: Session) -> db_User:
    db_user = get_user_by_id(uid=uid, session=session)
    if not db_user:
        raise UserNotFoundError("User not found")
    db_user.username = update_data.get("username", db_user.username)
    db_user.email = update_data.get("email", db_user.email)
    db_user.role = update_data.get("role", db_user.role)
    try:
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        session.rollback()
        raise UserExistsError("User with provided username or email already exists.")
    return db_user


def delete_user_data(uid: int, session: Session) -> int:
    db_user = get_user_by_id(uid=uid, session=session)
    if not db_user:
        raise UserNotFoundError
    session.delete(db_user)
    session.commit()
    return 1
