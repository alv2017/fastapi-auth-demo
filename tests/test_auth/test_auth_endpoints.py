class TestGetAccessToke:
    def test_get_access_token(self, client_with_non_empty_db, basic_user_data):
        test_client = client_with_non_empty_db
        user_data = basic_user_data
        form_data = {"username": user_data.get("username"), "password": user_data.get("password")}
        headers = {"content-type": "application/x-www-form-urlencoded"}

        response = test_client.post("/auth/token", data=form_data, headers=headers)
        actual_response_data = response.json()

        assert response.status_code == 200
        assert "access_token" in actual_response_data
        assert "token_type" in actual_response_data
        assert actual_response_data["token_type"] == "Bearer"

    def test_get_access_token_empty_form_data(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        form_data = {"username": "", "password": ""}
        headers = {"content-type": "application/x-www-form-urlencoded"}
        expected_response_data = {"detail": "Incorrect username or password"}

        response = test_client.post("/auth/token", data=form_data, headers=headers)
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_access_non_existing_user_data(self, client_with_non_empty_db, demo_user_data):
        test_client = client_with_non_empty_db
        user_data = demo_user_data
        form_data = {"username": user_data.get("username"), "password": user_data.get("password")}
        headers = {"content-type": "application/x-www-form-urlencoded"}
        expected_response_data = {"detail": "Incorrect username or password"}

        response = test_client.post("/auth/token", data=form_data, headers=headers)
        actual_response_data = response.json()
        assert response.status_code == 401
        assert actual_response_data == expected_response_data
