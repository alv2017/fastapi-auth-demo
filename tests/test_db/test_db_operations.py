from typing import Optional, Type

import pytest

from app.db.operations import (
    UserNotFoundError,
    add_user,
    delete_user_data,
    get_all_users,
    get_user,
    get_user_by_id,
    update_user_data,
)
from app.db.schema import User as db_User


class TestAddUser:
    def test_add_user_to_empty_db(self, session, demo_user_data):
        db_session = session
        user_data = demo_user_data

        db_user: Optional[db_User] = add_user(
            session=db_session, username=user_data["username"], email=user_data["email"], password=user_data["password"]
        )

        assert db_user is not None
        assert db_user.id == 1
        assert isinstance(db_user, db_User)

    def test_add_user_to_non_empty_db(self, non_empty_db_session, demo_user_data):
        db_session = non_empty_db_session
        user_data = demo_user_data

        db_user: Optional[db_User] = add_user(
            session=db_session, username=user_data["username"], email=user_data["email"], password=user_data["password"]
        )

        assert db_user is not None
        assert db_user.id > 0
        assert isinstance(db_user, db_User)

    def test_add_user_duplicate_user(self, non_empty_db_session, basic_user_data):
        db_session = non_empty_db_session
        user_data = basic_user_data

        db_user: Optional[db_User] = add_user(
            session=db_session, username=user_data["username"], email=user_data["email"], password=user_data["password"]
        )

        assert db_user is None


class TestGetUser:
    def test_get_user_by_username(self, non_empty_db_session, basic_user):
        db_session = non_empty_db_session
        db_session.refresh(basic_user)
        username = basic_user.username
        expected_user: db_User = basic_user

        actual_user = get_user(session=db_session, username_or_email=username)

        assert actual_user is not None
        assert isinstance(actual_user, db_User)
        assert actual_user == expected_user

    def test_get_user_by_email(self, non_empty_db_session, basic_user):
        db_session = non_empty_db_session
        db_session.refresh(basic_user)
        email = basic_user.email
        expected_user: db_User = basic_user

        actual_user = get_user(session=db_session, username_or_email=email)

        assert actual_user is not None
        assert isinstance(actual_user, db_User)
        assert actual_user == expected_user

    def test_get_user_when_username_not_exists(self, non_empty_db_session):
        db_session = non_empty_db_session
        username = "non-existing-username"
        actual_user = get_user(session=db_session, username_or_email=username)
        assert actual_user is None

    def test_get_user_when_email_not_exists(self, non_empty_db_session):
        db_session = non_empty_db_session
        email = "non-existing-username@gmail.com"
        actual_user = get_user(session=db_session, username_or_email=email)
        assert actual_user is None


class TestGetAllUsers:
    def test_get_all_users(self, non_empty_db_session):
        db_session = non_empty_db_session
        users: list[Type[db_User]] = get_all_users(db_session)

        assert isinstance(users, list)

        for user in users:
            assert isinstance(user, db_User)
        assert len(users) > 0

    def test_get_all_users_empty_table(self, session):
        db_session = session
        users: list[Type[db_User]] = get_all_users(db_session)
        assert isinstance(users, list)
        assert len(users) == 0


class TestGetUserById:
    def test_get_user_by_id(self, non_empty_db_session):
        db_session = non_empty_db_session
        uid = 1

        user = get_user_by_id(uid=uid, session=db_session)

        assert user is not None
        assert isinstance(user, db_User)
        assert user.id == uid

    def test_get_user_by_id_non_existing_user_id(self, session):
        db_session = session
        uid = 1
        user = get_user_by_id(uid=uid, session=db_session)
        assert user is None


class TestUpdateUserData:
    def test_update_user_data(self, non_empty_db_session, basic_user):
        db_session = non_empty_db_session
        db_session.refresh(basic_user)
        initial_id = basic_user.id
        initial_username = basic_user.username
        initial_email = basic_user.email
        update_data = {"username": "updated_name", "email": "updated_email@example.com"}

        updated_user = update_user_data(uid=initial_id, update_data=update_data, session=db_session)

        assert isinstance(updated_user, db_User)
        assert updated_user.id == initial_id
        assert updated_user.username != initial_username
        assert updated_user.email != initial_email

    def test_update_user_data_role_update(self, non_empty_db_session, basic_user):
        db_session = non_empty_db_session
        db_session.refresh(basic_user)
        initial_id = basic_user.id
        initial_role = basic_user.role
        new_role = "staff"
        update_data = {"role": new_role}

        updated_user = update_user_data(uid=initial_id, update_data=update_data, session=db_session)

        assert isinstance(updated_user, db_User)
        assert initial_role != new_role
        assert updated_user.id == initial_id
        assert updated_user.role == new_role

    def test_update_user_data_non_existing_user(self, session):
        db_session = session
        non_existing_id = 1

        update_data = {"username": "updated_name", "email": "updated_email@example.com"}

        with pytest.raises(UserNotFoundError):
            update_user_data(uid=non_existing_id, update_data=update_data, session=db_session)


class TestDeleteUserData:
    def test_delete_user_data(self, non_empty_db_session):
        db_session = non_empty_db_session
        id_to_delete = 1
        result = delete_user_data(uid=id_to_delete, session=db_session)
        assert result == 1
        assert db_session.query(db_User).filter(db_User.id == id_to_delete).first() is None

    def test_delete_user_data_non_existing_user_id(self, session):
        db_session = session
        non_existing_user_id = 1
        with pytest.raises(UserNotFoundError):
            delete_user_data(uid=non_existing_user_id, session=db_session)
