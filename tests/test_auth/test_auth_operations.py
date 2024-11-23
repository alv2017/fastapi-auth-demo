from app.auth.operations import authenticate_user
from app.db.schema import User as db_User


class TestAuthenticateUser:
    def test_authenticate_user_by_username_existing_user(self, non_empty_db_session, basic_user_data):
        db_session = non_empty_db_session
        user_data: dict = basic_user_data
        username_or_email = user_data["username"]
        password = user_data["password"]

        user = authenticate_user(session=db_session, username_or_email=username_or_email, password=password)

        assert user is not None
        assert isinstance(user, db_User)

    def test_authenticate_user_by_email_existing_user(self, non_empty_db_session, basic_user_data):
        db_session = non_empty_db_session
        user_data: dict = basic_user_data
        username_or_email = user_data["email"]
        password = user_data["password"]

        user = authenticate_user(session=db_session, username_or_email=username_or_email, password=password)

        assert user is not None
        assert isinstance(user, db_User)

    def test_authenticate_user_invalid_password(self, non_empty_db_session, basic_user_data):
        db_session = non_empty_db_session
        user_data: dict = basic_user_data
        username_or_email1 = user_data["email"]
        username_or_email2 = user_data["username"]
        password = "this_password_is_invalid"

        user1 = authenticate_user(session=db_session, username_or_email=username_or_email1, password=password)

        user2 = authenticate_user(session=db_session, username_or_email=username_or_email2, password=password)

        assert user1 is None
        assert user2 is None

    def test_authenticate_user_non_existing_user(self, non_empty_db_session, demo_user_data):
        db_session = non_empty_db_session
        user_data: dict = demo_user_data

        username_or_email1 = user_data["username"]
        password1 = user_data["password"]

        username_or_email2 = user_data["email"]
        password2 = user_data["password"]

        user1 = authenticate_user(session=db_session, username_or_email=username_or_email1, password=password1)

        user2 = authenticate_user(session=db_session, username_or_email=username_or_email2, password=password2)

        assert user1 is None
        assert user2 is None
