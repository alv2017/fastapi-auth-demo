from datetime import UTC, datetime, timedelta
from typing import Optional

from jose import jwt

from app.auth.token import create_access_token, decode_access_token
from app.db.schema import User as db_User

from app.settings import test_settings as settings


ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY


class TestCreateToken:
    def test_create_token(self, basic_user):
        user = basic_user
        token_data = {"sub": user.username}
        access_token = create_access_token(
            data=token_data,
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
        )
        decoded_access_token_data = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)

        assert isinstance(access_token, str)
        assert len(access_token) > 0
        assert "sub" in decoded_access_token_data
        assert "exp" in decoded_access_token_data
        assert decoded_access_token_data["sub"] == token_data["sub"]

    def test_create_token_set_custom_expiry_time(self, basic_user):
        token_live_time_seconds = 300
        token_expiration_time = (datetime.now(tz=UTC) + timedelta(seconds=token_live_time_seconds)).timestamp()
        token_data = {"sub": basic_user.username, "exp": token_expiration_time}
        access_token = create_access_token(
            data=token_data,
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
        )
        decoded_access_token_data = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)

        assert isinstance(access_token, str)
        assert len(access_token) > 0
        assert "sub" in decoded_access_token_data
        assert "exp" in decoded_access_token_data
        assert decoded_access_token_data["sub"] == token_data["sub"]
        assert decoded_access_token_data["exp"] == token_data["exp"]


class TestDecodeAccessToken:
    def test_decode_access_token(self, non_empty_db_session, basic_user, basic_user_token):
        db_session = non_empty_db_session
        db_session.refresh(basic_user)
        access_token = basic_user_token

        expected_user = basic_user

        result = db_session.query(db_User).filter(db_User.username == basic_user.username).first()

        actual_user: Optional[db_User] = decode_access_token(
            token=access_token,
            session=db_session,
            secret_key=SECRET_KEY,
            algorithms=ALGORITHM
        )

        assert actual_user is not None
        assert isinstance(actual_user, db_User)
        assert actual_user == expected_user

    def test_decode_token_existing_user_expired_token(self, non_empty_db_session, basic_user_token_expired):
        db_session = non_empty_db_session
        token = basic_user_token_expired
        user: Optional[db_User] = decode_access_token(
            token=token,
            session=db_session,
            secret_key=SECRET_KEY,
            algorithms=ALGORITHM
        )
        assert user is None

    def test_decode_token_non_existing_user(self, session, basic_user_token):
        db_session = session
        token = basic_user_token
        user: Optional[db_User] = decode_access_token(
            token=token,
            session=db_session,
            secret_key=SECRET_KEY,
            algorithms=ALGORITHM
        )
        assert user is None

    def test_decode_token_invalid_token(self, non_empty_db_session):
        db_session = non_empty_db_session
        token = "invalid.token.string"
        user: Optional[db_User] = decode_access_token(
            token=token,
            session=db_session,
            secret_key=SECRET_KEY,
            algorithms=ALGORITHM
        )
        assert user is None
