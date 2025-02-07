import pytest
from fastapi import HTTPException

from app.db.schema import User as db_User
from app.users.permissions import (
    authenticated_admin_user,
    authenticated_staff_user,
    authenticated_user,
)


class TestAuthenticatedUser:
    def test_authenticated_user(self, non_empty_db_session, basic_user, basic_user_token):
        db_session = non_empty_db_session
        access_token = basic_user_token
        db_session.refresh(basic_user)
        expected_auth_user = basic_user

        actual_auth_user = authenticated_user(token=access_token, session=db_session)

        assert isinstance(actual_auth_user, db_User)
        assert actual_auth_user == expected_auth_user

    def test_authenticated_user_when_token_expired(self, non_empty_db_session, basic_user, basic_user_token_expired):
        db_session = non_empty_db_session
        access_token = basic_user_token_expired

        with pytest.raises(HTTPException):
            authenticated_user(token=access_token, session=db_session)

    def test_authenticated_user_when_token_invalid(self, non_empty_db_session):
        db_session = non_empty_db_session
        access_token = "invalid.token.string"

        with pytest.raises(HTTPException):
            authenticated_user(token=access_token, session=db_session)


class TestAuthenticatedStaffUser:
    def test_authenticated_staff_user(self, non_empty_db_session, staff_user, staff_user_token):
        db_session = non_empty_db_session
        db_session.refresh(staff_user)
        access_token = staff_user_token
        expected_user = staff_user

        actual_user = authenticated_staff_user(token=access_token, session=db_session)

        assert isinstance(actual_user, db_User)
        assert actual_user == expected_user

    def test_authenticated_staff_user_when_token_expired(self, non_empty_db_session, staff_user_token_expired):
        db_session = non_empty_db_session
        access_token = staff_user_token_expired

        with pytest.raises(HTTPException):
            authenticated_staff_user(token=access_token, session=db_session)

    def test_authenticated_staff_user_when_token_invalid(self, non_empty_db_session):
        db_session = non_empty_db_session
        access_token = "invalid.token.string"

        with pytest.raises(HTTPException):
            authenticated_staff_user(token=access_token, session=db_session)

    def test_authenticated_staff_user_when_basic_user_token(self, non_empty_db_session, basic_user_token):
        db_session = non_empty_db_session
        access_token = basic_user_token

        with pytest.raises(HTTPException):
            authenticated_staff_user(token=access_token, session=db_session)

    def test_authenticated_staff_user_when_admin_user_token(self, non_empty_db_session, admin_user_token):
        db_session = non_empty_db_session
        access_token = admin_user_token

        with pytest.raises(HTTPException):
            authenticated_staff_user(token=access_token, session=db_session)


class TestAuthenticatedAdminUser:
    def test_authenticated_admin_user(self, non_empty_db_session, admin_user, admin_user_token):
        db_session = non_empty_db_session
        db_session.refresh(admin_user)
        access_token = admin_user_token
        expected_user = admin_user

        actual_user = authenticated_admin_user(token=access_token, session=db_session)

        assert isinstance(actual_user, db_User)
        assert actual_user == expected_user

    def test_authenticated_admin_user_when_token_expired(self, non_empty_db_session, admin_user_token_expired):
        db_session = non_empty_db_session
        access_token = admin_user_token_expired

        with pytest.raises(HTTPException):
            authenticated_admin_user(token=access_token, session=db_session)

    def test_authenticated_admin_user_when_token_invalid(self, non_empty_db_session):
        db_session = non_empty_db_session
        access_token = "invalid.token.string"

        with pytest.raises(HTTPException):
            authenticated_admin_user(token=access_token, session=db_session)

    def test_authenticated_admin_user_when_basic_user_token(self, non_empty_db_session, basic_user_token):
        db_session = non_empty_db_session
        access_token = basic_user_token

        with pytest.raises(HTTPException):
            authenticated_admin_user(token=access_token, session=db_session)

    def test_authenticated_admin_user_when_staff_user_token(self, non_empty_db_session, staff_user_token):
        db_session = non_empty_db_session
        access_token = staff_user_token

        with pytest.raises(HTTPException):
            authenticated_admin_user(token=access_token, session=db_session)
