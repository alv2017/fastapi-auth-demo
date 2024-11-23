class TestRegisterNewUser:
    def test_register_new_user_empty_db(self, client, demo_user_data):
        test_client = client
        expected_user_id = 1
        user_data = demo_user_data
        expected_user_data = {
            "id": expected_user_id,
            "username": user_data["username"],
            "email": user_data["email"],
        }

        response = test_client.post("/register/", json=user_data)
        actual_response_data = response.json()

        assert response.status_code == 201
        assert actual_response_data == expected_user_data

    def test_register_new_user_non_empty_db(self, client_with_non_empty_db, demo_user_data):
        test_client = client_with_non_empty_db
        user_data = demo_user_data
        response = test_client.post("/register/", json=user_data)
        actual_response_data = response.json()

        assert response.status_code == 201
        assert "id" in actual_response_data
        assert actual_response_data["id"] > 0
        assert "username" in actual_response_data
        assert actual_response_data["username"] == user_data["username"]
        assert "email" in actual_response_data
        assert actual_response_data["email"] == user_data["email"]

    def test_register_new_user_duplicate_user(self, client_with_non_empty_db, basic_user):
        test_client = client_with_non_empty_db
        user_data: dict = {"username": basic_user.username, "email": basic_user.email, "password": "basic_password"}
        expected_response_data = {"detail": "User with provided username or email already exists"}

        response = test_client.post("/register/", json=user_data)
        actual_response_data = response.json()

        assert response.status_code == 409
        assert actual_response_data == expected_response_data


class TestGetUserMe:
    def test_get_user_me_authenticated(self, client_basic, basic_user):
        test_client = client_basic
        auth_user = basic_user
        expected_response_data = {"id": auth_user.id, "username": auth_user.username, "email": auth_user.email}

        response = test_client.get("/users/me/")
        actual_response_data = response.json()

        assert response.status_code == 200
        assert actual_response_data == expected_response_data

    def test_get_user_me_unauthenticated(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        expected_response_data = {"detail": "Not authenticated"}

        response = test_client.get("/users/me")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_user_me_expired_token(self, client_basic_expired):
        test_client = client_basic_expired
        expected_response_data = {"detail": "Access forbidden"}

        response = test_client.get("/users/me/")
        actual_response_data = response.json()

        assert response.status_code == 403
        assert actual_response_data == expected_response_data
