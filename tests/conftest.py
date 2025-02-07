from datetime import UTC, datetime, timedelta
from typing import Generator, Optional

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import QueuePool, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.auth.token import create_access_token
from app.db.connection import get_session
from app.db.schema import Base
from app.db.schema import User as db_User
from app.main import app
from app.settings import pwd_context
from app.settings import settings

# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# ALGORITHM = settings.ALGORITHM
# DATABASE_URL = settings.DATABASE_URL
# SECRET_KEY = settings.SECRET_KEY


def add_db_user(user: db_User, session: Session) -> Optional[db_User]:
    try:
        session.add(user)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        return
    session.refresh(user)
    return user


def auth_client(session: Session, user: db_User, expired=False) -> TestClient:
    auth_user: db_User = add_db_user(session=session, user=user)
    token_data = {"sub": auth_user.username}
    if expired:
        token_expiration_time = {"exp": (datetime.now(tz=UTC) - timedelta(minutes=1)).timestamp()}
        token_data.update(token_expiration_time)

    access_token = create_access_token(token_data)
    headers = {"Authorization": f"Bearer {access_token}"}
    app.dependency_overrides |= {get_session: lambda: session}
    test_client = TestClient(app)
    test_client.headers.update(headers)
    return test_client


@pytest.fixture
def demo_user_data():
    return {"username": "demo", "email": "demo@example.com", "password": "hello_demo"}


@pytest.fixture
def basic_user_data() -> dict:
    return {
        "username": "basic_user",
        "email": "basic_user@gmail.com",  # valid email domain is required when validating an email address
        "password": "hello_basic_user",
    }


@pytest.fixture
def basic_user(basic_user_data) -> db_User:
    return db_User(
        username=basic_user_data.get("username"),
        email=basic_user_data.get("email"),
        hashed_password=pwd_context.hash(basic_user_data.get("password")),
    )


@pytest.fixture
def basic_user_token(basic_user):
    user: db_User = basic_user
    token_data = {
        "sub": user.username,
        "exp": datetime.now(tz=UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token: str = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


@pytest.fixture
def basic_user_token_expired(basic_user):
    user: db_User = basic_user
    token_data = {"sub": user.username, "exp": datetime.now(tz=UTC) - timedelta(minutes=1)}
    token: str = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


@pytest.fixture
def staff_user() -> db_User:
    return db_User(
        username="staff_user",
        email="staff_user@example.com",
        hashed_password=pwd_context.hash("hello_staff_user"),
        role="staff",
    )


@pytest.fixture
def staff_user_token(staff_user):
    user: db_User = staff_user
    token_data = {
        "sub": user.username,
        "exp": datetime.now(tz=UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token: str = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


@pytest.fixture
def staff_user_token_expired(staff_user):
    user: db_User = staff_user
    token_data = {"sub": user.username, "exp": datetime.now(tz=UTC) - timedelta(minutes=1)}
    token: str = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


@pytest.fixture
def admin_user() -> db_User:
    return db_User(
        username="admin_user",
        email="admin_user@example.com",
        hashed_password=pwd_context.hash("hello_admin_user"),
        role="admin",
    )


@pytest.fixture
def admin_user_token(admin_user):
    user: db_User = admin_user
    token_data = {
        "sub": user.username,
        "exp": datetime.now(tz=UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token: str = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


@pytest.fixture
def admin_user_token_expired(admin_user):
    user: db_User = admin_user
    token_data = {"sub": user.username, "exp": datetime.now(tz=UTC) - timedelta(minutes=1)}
    token: str = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=QueuePool,
    )
    session_local = sessionmaker(engine)
    db_session = session_local()
    Base.metadata.create_all(bind=engine)

    yield db_session

    Base.metadata.drop_all(bind=engine)
    db_session.close()


@pytest.fixture(scope="function")
def non_empty_db_session(session, basic_user, staff_user, admin_user) -> Generator[Session, None, None]:
    users: list[db_User] = [basic_user, staff_user, admin_user]
    for user in users:
        session.add(user)
    session.commit()
    yield session


@pytest.fixture
def client(session):
    app.dependency_overrides |= {get_session: lambda: session}
    test_client = TestClient(app)
    return test_client


@pytest.fixture
def client_with_non_empty_db(non_empty_db_session):
    db_session = non_empty_db_session
    app.dependency_overrides |= {get_session: lambda: db_session}
    test_client = TestClient(app)
    return test_client


@pytest.fixture
def client_basic(non_empty_db_session, basic_user) -> Generator[TestClient, None, None]:
    test_client: TestClient = auth_client(session=non_empty_db_session, user=basic_user)
    yield test_client
    test_client.headers.clear()


@pytest.fixture
def client_basic_expired(non_empty_db_session, basic_user) -> Generator[TestClient, None, None]:
    test_client: TestClient = auth_client(session=non_empty_db_session, user=basic_user, expired=True)
    yield test_client
    test_client.headers.clear()


@pytest.fixture
def client_staff(non_empty_db_session, staff_user):
    test_client: TestClient = auth_client(session=non_empty_db_session, user=staff_user)
    yield test_client
    test_client.headers.clear()


@pytest.fixture
def client_staff_expired(non_empty_db_session, staff_user):
    test_client: TestClient = auth_client(session=non_empty_db_session, user=staff_user, expired=True)
    yield test_client
    test_client.headers.clear()


@pytest.fixture
def client_admin(non_empty_db_session, admin_user):
    test_client: TestClient = auth_client(session=non_empty_db_session, user=admin_user)
    yield test_client
    test_client.headers.clear()


@pytest.fixture
def client_admin_expired(non_empty_db_session, admin_user):
    test_client: TestClient = auth_client(session=non_empty_db_session, user=admin_user, expired=True)
    yield test_client
    test_client.headers.clear()
