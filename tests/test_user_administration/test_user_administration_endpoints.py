import pytest
from typing import Optional

from app.db.schema import User as db_User
from app.users.models import UserWithRole, UserWithRoleCreate


@pytest.fixture
def new_basic_user():
    return UserWithRoleCreate(
        username="new_basic_user",
        email="new_basic_user@example.com",
        role="basic",
        password="basic_secret"
    )


@pytest.fixture
def new_staff_user():
    return UserWithRoleCreate(
        username="new_staff_user",
        email="new_staff_user@example.com",
        role="staff",
        password="staff_secret"
    )


@pytest.fixture
def new_admin_user():
    return UserWithRoleCreate(
        username="new_admin_user",
        email="new_admin_user@example.com",
        role="admin",
        password="admin_secret"
    )


@pytest.fixture
def user_update_data():
    return {
            "username": "updated_username",
            "email": "updatated_username@example.com"
    }



class TestCreateUser:
    def test_create_user_basic(self, new_basic_user, client_admin):
        new_user: UserWithRoleCreate = new_basic_user
        test_client = client_admin
        expected_username = new_user.username
        expected_email = new_user.email
        expected_role = new_user.role

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 201
        assert "id" in actual_response_data
        assert actual_response_data["id"] > 0
        assert "username" in actual_response_data
        assert actual_response_data["username"] == expected_username
        assert "email" in actual_response_data
        assert actual_response_data["email"] == expected_email
        assert "role" in actual_response_data
        assert actual_response_data["role"] == expected_role
        assert "password" not in actual_response_data

    def test_create_user_staff(self, new_staff_user, client_admin):
        new_user: UserWithRoleCreate = new_staff_user
        test_client = client_admin
        expected_username = new_user.username
        expected_email = new_user.email
        expected_role = new_user.role

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 201
        assert "id" in actual_response_data
        assert actual_response_data["id"] > 0
        assert "username" in actual_response_data
        assert actual_response_data["username"] == expected_username
        assert "email" in actual_response_data
        assert actual_response_data["email"] == expected_email
        assert "role" in actual_response_data
        assert actual_response_data["role"] == expected_role
        assert "password" not in actual_response_data

    def test_create_user_admin(self, new_admin_user, client_admin):
        new_user: UserWithRoleCreate = new_admin_user
        test_client = client_admin
        expected_username = new_user.username
        expected_email = new_user.email
        expected_role = new_user.role

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 201
        assert "id" in actual_response_data
        assert actual_response_data["id"] > 0
        assert "username" in actual_response_data
        assert actual_response_data["username"] == expected_username
        assert "email" in actual_response_data
        assert actual_response_data["email"] == expected_email
        assert "role" in actual_response_data
        assert actual_response_data["role"] == expected_role
        assert "password" not in actual_response_data

    def test_create_user_duplicated_user(self, basic_user_data, client_admin):
        user_data = basic_user_data
        new_user = UserWithRoleCreate(
            username=user_data.get("username"),
            email=user_data.get("email"),
            role="basic",
            password=user_data.get("password")
        )
        test_client = client_admin
        expected_response_data = {
            "detail": "Username or email already exists"
        }

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 409
        assert actual_response_data == expected_response_data

    def test_create_user_expired_admin_token(self, new_basic_user, client_admin_expired):
        new_user: UserWithRoleCreate = new_basic_user
        test_client = client_admin_expired
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_create_user_unauthenticated_user_cant_perform_operation(self, new_basic_user, client):
        new_user: UserWithRoleCreate = new_basic_user
        test_client = client
        expected_response_data = {"detail": "Not authenticated"}

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_create_user_basic_user_cant_perform_operation(self, new_basic_user, client_basic):
        new_user: UserWithRoleCreate = new_basic_user
        test_client = client_basic
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_create_user_staff_user_cant_perform_operation(self, new_basic_user, client_staff):
        new_user: UserWithRoleCreate = new_basic_user
        test_client = client_staff
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.post("/users/", json=new_user.model_dump())
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data


class TestGetUserList:
    def test_get_user_list(self, client_admin):
        test_client = client_admin

        response = test_client.get("/users/")
        response_data = response.json()

        assert response.status_code == 200
        assert isinstance(response_data, list)
        assert len(response_data) > 0

        for item in response_data:
            assert isinstance(item, dict)
            assert "id" in item
            assert "username" in item
            assert "email" in item
            assert "role" in item

    def test_get_user_list_admin_token_expired(self, client_admin_expired):
        test_client = client_admin_expired
        expected_response_date = {"detail": "Unauthorized access"}

        response = test_client.get("/users/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_date

    def test_get_user_list_unauthenticated_user_cant_perform_operation(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        expected_response_date = {"detail": "Not authenticated"}

        response = test_client.get("/users/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_date

    def test_get_user_list_basic_user_cant_perform_operation(self, client_basic):
        test_client = client_basic
        expected_response_date = {"detail": "Unauthorized access"}

        response = test_client.get("/users/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_date

    def test_get_user_list_staff_user_cant_perform_operation(self, client_staff):
        test_client = client_staff
        expected_response_date = {"detail": "Unauthorized access"}

        response = test_client.get("/users/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_date


class TestGetUser:
    def test_get_user(self, client_admin):
        test_client = client_admin
        user_id = 1

        response = test_client.get(f"/users/{user_id}/")
        actual_response_data = response.json()

        assert response.status_code == 200
        assert "id" in actual_response_data
        assert actual_response_data.get("id") > 0
        assert "username" in actual_response_data
        assert "email" in actual_response_data
        assert "role" in actual_response_data

    def test_get_user_when_user_not_exist(self, client_admin, non_empty_db_session):
        test_client = client_admin
        db_session = non_empty_db_session
        user_id = 1234
        expected_response_data = {
            "detail": "User not found"
        }

        response = test_client.get(f"/users/{user_id}/")
        actual_response_data = response.json()

        assert db_session.query(db_User).filter(db_User.id == user_id).first() is None
        assert response.status_code == 404
        assert actual_response_data == expected_response_data

    def test_get_user_expired_admin_token(self, client_admin_expired):
        test_client = client_admin_expired
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.get(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_user_unauthorized_user_cant_perform_operation(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        user_id = 1
        expected_response_data = {
            "detail": "Not authenticated"
        }

        response = test_client.get(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_user_basic_user_cant_perform_operation(self, client_basic):
        test_client = client_basic
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.get(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_user_staff_user_cant_perform_operation(self, client_staff):
        test_client = client_staff
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.get(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data


class TestUpdateUser:
    def test_update_user(self, client_admin, non_empty_db_session, user_update_data):
        test_client = client_admin
        db_session = non_empty_db_session
        user_id = 1
        user_to_update: Optional[db_User] = db_session.query(db_User).filter(db_User.id == user_id).first()

        # before update
        assert user_to_update is not None
        assert user_to_update.username != user_update_data.get("username")
        assert user_to_update.email != user_update_data.get("email")

        response = test_client.patch(f"/users/{user_id}/", json=user_update_data)
        actual_response_data = response.json()

        assert response.status_code == 200
        assert "id" in actual_response_data
        assert actual_response_data.get("id") == user_id
        assert "username" in actual_response_data
        assert actual_response_data.get("username") == user_update_data.get("username")
        assert "email" in actual_response_data
        assert actual_response_data.get("email") == user_update_data.get("email")

        # after update
        db_session.refresh(user_to_update)
        assert user_to_update.username == user_update_data.get("username")
        assert user_to_update.email == user_update_data.get("email")

    def test_update_user_expired_admin_token(self, client_admin_expired, user_update_data):
        test_client = client_admin_expired
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.patch(f"/users/{user_id}/", json=user_update_data)
        actual_response_data = response.json()

        assert response.status_code == 401
        assert expected_response_data == actual_response_data

    def test_update_user_non_existing_user_id(self, client_admin, non_empty_db_session, user_update_data):
        test_client = client_admin
        db_session = non_empty_db_session
        user_id = 1234
        expected_response_data = {
            "detail": "User not found"
        }

        response = test_client.patch(f"/users/{user_id}/", json=user_update_data)
        actual_response_data = response.json()

        assert response.status_code == 404
        assert db_session.query(db_User).filter(db_User.id == user_id).first() is None
        assert actual_response_data == expected_response_data

    def test_update_use_uauthenticated_user_cant_perform_operation(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        user_id = 1
        expected_response_data = {
            "detail": "Not authenticated"
        }

        response = test_client.patch(f"/users/{user_id}/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_update_use_basic_user_cant_perform_operation(self, client_basic):
        test_client = client_basic
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.patch(f"/users/{user_id}/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_update_use_staff_user_cant_perform_operation(self, client_staff):
        test_client = client_staff
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.patch(f"/users/{user_id}/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data


class TestDeleteUser:
    def test_delete_user(self, client_admin, non_empty_db_session):
        test_client = client_admin
        db_session = non_empty_db_session
        user_id = 1
        user_to_be_deleted = db_session.query(db_User).filter(db_User.id == user_id).first()

        # before delete
        assert user_to_be_deleted is not None
        assert isinstance(user_to_be_deleted, db_User)

        response = test_client.delete(f"/users/{user_id}")

        # after delete
        assert response.status_code == 204
        assert db_session.query(db_User).filter(db_User.id == user_id).first() is None

    def test_delete_user_non_existing_user_id(self, client_admin, non_empty_db_session):
        test_client = client_admin
        db_session = non_empty_db_session
        user_id = 1234
        expected_response_data = {
            "detail": "User not found"
        }

        # user with given id does not exist in test database
        assert db_session.query(db_User).filter(db_User.id == user_id).first() is None

        response = test_client.delete(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 404
        assert actual_response_data == expected_response_data

    def test_delete_user_admin_token_expired(self, client_admin_expired):
        test_client = client_admin_expired
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.delete(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_delete_user_unauthorized_user_cant_perform_operation(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        user_id = 1
        expected_response_data = {
            "detail": "Not authenticated"
        }

        response = test_client.delete(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_delete_user_basic_user_cant_perform_operation(self, client_basic):
        test_client = client_basic
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.delete(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_delete_user_staff_user_cant_perform_operation(self, client_staff):
        test_client = client_staff
        user_id = 1
        expected_response_data = {
            "detail": "Unauthorized access"
        }

        response = test_client.delete(f"/users/{user_id}")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data
