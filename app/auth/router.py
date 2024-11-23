from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.connection import get_session
from app.db.schema import User as db_User

from .operations import authenticate_user
from .token import Token, create_access_token

router = APIRouter()


@router.post("/auth/token/")
def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
) -> Token:
    user: Optional[db_User] = authenticate_user(
        session=session, username_or_email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token_creation_data = {"sub": user.username}
    access_token: str = create_access_token(data=token_creation_data)
    return Token(access_token=access_token)
