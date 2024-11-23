from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.token import decode_access_token
from app.db.connection import get_session
from app.db.operations import add_user
from app.db.schema import User as db_User
from app.settings import oauth2_scheme

from .models import UserCreate, UserResponse

router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED)
def register_new_user(user: UserCreate, session: Session = Depends(get_session)) -> UserResponse:
    new_user: db_User = add_user(session=session, username=user.username, email=user.email, password=user.password)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User with provided username or email already exists"
        )

    response = UserResponse(id=new_user.id, username=new_user.username, email=new_user.email)

    return response


@router.get("/users/me/", status_code=status.HTTP_200_OK)
def get_user_me(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> UserResponse:
    user: db_User = decode_access_token(token=token, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
    response = UserResponse(id=user.id, username=user.username, email=user.email)
    return response
