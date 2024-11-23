from pydantic import BaseModel

from app.db.schema import Role


class User(BaseModel):
    username: str
    email: str


class UserWithRole(User):
    role: Role


class UserCreate(User):
    password: str


class UserWithRoleCreate(UserWithRole):
    password: str


class UserResponse(User):
    id: int


class UserWithRoleResponse(UserWithRole):
    id: int
