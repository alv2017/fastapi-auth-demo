from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.token import decode_access_token
from app.db.connection import get_session
from app.db.schema import Role
from app.db.schema import User as db_User
from app.settings import oauth2_scheme, settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def authenticated_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> db_User:
    auth_user = decode_access_token(
        token=token, session=session, secret_key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
    )
    if not auth_user:
        if not auth_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    return auth_user


def authenticated_staff_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> db_User:
    auth_user = authenticated_user(token=token, session=session)
    if auth_user.role != Role.staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    return auth_user


def authenticated_admin_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> db_User:
    auth_user: db_User = authenticated_user(token=token, session=session)
    if auth_user.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    return auth_user


def authenticated_staff_or_admin_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> db_User:
    auth_user: db_User = authenticated_user(token=token, session=session)
    if auth_user.role not in [Role.staff, Role.admin]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")

    return auth_user
