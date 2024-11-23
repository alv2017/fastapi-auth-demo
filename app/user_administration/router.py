from typing import Optional, Type

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_session
from app.db.operations import (
    UserExistsError,
    UserNotFoundError,
    add_user,
    delete_user_data,
    get_all_users,
    get_user_by_id,
    update_user_data,
)
from app.db.schema import User as db_User
from app.settings import oauth2_scheme
from app.users.models import UserWithRoleCreate, UserWithRoleResponse
from app.users.permissions import authenticated_admin_user

router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserWithRoleCreate,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_admin_user),
) -> UserWithRoleResponse:

    new_user: db_User = add_user(
        session=session, username=user.username, email=user.email, password=user.password, role=user.role
    )

    if not new_user:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Username or email already exists")

    response = UserWithRoleResponse(
        id=new_user.id, username=new_user.username, email=new_user.email, role=new_user.role
    )

    return response


@router.get("/users/")
def get_user_list(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_admin_user),
) -> list[UserWithRoleResponse]:

    users: list[Type[db_User]] = get_all_users(session=session)

    response = [
        UserWithRoleResponse(id=user.id, username=user.username, email=user.email, role=user.role) for user in users
    ]

    return response


@router.get("/users/{uid}")
def get_user(
    uid: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_admin_user),
) -> UserWithRoleResponse:

    user: Optional[db_User] = get_user_by_id(uid=uid, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    response = UserWithRoleResponse(id=user.id, username=user.username, email=user.email, role=user.role)

    return response


@router.patch("/users/{uid}")
def update_user(
    uid: int,
    update_data: dict,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_admin_user),
) -> UserWithRoleResponse:

    try:
        user: Optional[db_User] = update_user_data(uid=uid, update_data=update_data, session=session)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except UserExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with provided username or email already exists"
        )

    response = UserWithRoleResponse(id=user.id, username=user.username, email=user.email, role=user.role)

    return response


@router.delete("/users/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    uid: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_admin_user),
):
    try:
        delete_user_data(uid=uid, session=session)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {}
