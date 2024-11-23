
class TestWelcome:
    def test_welcome(self, client):
        test_client = client
        expected_response_data = {"api": "User Authentication Demo", "version": "v1"}

        response = test_client.get("/")
        actual_response_data = response.json()

        assert response.status_code == 200
        assert actual_response_data == expected_response_data


class TestGetFinancialNews:
    def test_get_financial_news(self, client_basic, basic_user):
        auth_user = basic_user
        test_client = client_basic
        expected_response_data = {
            "title": "The Latest News from the Financial Markets",
            "description": "Financial news can be accessed by members only.",
            "message": f"Hi, {auth_user.username}!",
        }

        response = test_client.get("/financial-markets/")
        actual_response_data = response.json()

        assert response.status_code == 200
        assert actual_response_data == expected_response_data

    def test_get_financial_news_unauthenticated_user(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        expected_response_data = {"detail": "Not authenticated"}

        response = test_client.get("/financial-markets/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_financial_news_expired_token(self, client_basic_expired):
        test_client = client_basic_expired
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.get("/financial-markets/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data


class TestGetStaffUpdates:
    def test_get_staff_updates(self, client_staff, staff_user):
        test_client = client_staff
        auth_user = staff_user
        expected_response_data = {
            "title": "Company Insights",
            "description": "Company Insights can be accessed only by members of staff",
            "message": f"Hi, {auth_user.username}! Stay up to date with the latest Company events!",
        }

        response = test_client.get("/company-insights")
        actual_response_data = response.json()

        assert response.status_code == 200
        assert actual_response_data == expected_response_data

    def test_get_staff_updates_unauthenticated_user(self, client_with_non_empty_db):
        test_client = client_with_non_empty_db
        expected_response_data = {"detail": "Not authenticated"}

        response = test_client.get("/company-insights/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_staff_updates_expired_token(self, client_staff_expired):
        test_client = client_staff_expired
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.get("/company-insights/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_staff_updates_no_access_for_basic_user(self, client_basic):
        test_client = client_basic
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.get("/company-insights/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_get_staff_updates_no_access_for_admin_user(self, client_admin):
        test_client = client_admin
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.get("/company-insights/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data


class TestAccessSystemAdministrationResources:
    def test_access_system_administration(self, client_admin, admin_user):
        test_client = client_admin
        auth_user = admin_user
        expected_response_data = {
            "title": "System Administration",
            "description": "System Administration resources can be accessed only by administrators only",
            "message": f"Hi, {auth_user.username}! Welcome to System Administration.",
        }

        response = test_client.get("/system-administration/")
        actual_response_data = response.json()

        assert response.status_code == 200
        assert actual_response_data == expected_response_data

    def test_access_system_administration_expired_admin_token(self, client_admin_expired):
        test_client = client_admin_expired
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.get("/system-administration/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_access_system_administration_no_access_for_unauthenticated_user(self, client):
        test_client = client
        expected_response_data = {"detail": "Not authenticated"}

        response = test_client.get("/system-administration/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_access_system_administration_no_access_for_basic_users(self, client_basic):
        test_client = client_basic
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.get("/system-administration/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data

    def test_access_system_administration_no_access_for_staff_users(self, client_staff):
        test_client = client_staff
        expected_response_data = {"detail": "Unauthorized access"}

        response = test_client.get("/system-administration/")
        actual_response_data = response.json()

        assert response.status_code == 401
        assert actual_response_data == expected_response_data
