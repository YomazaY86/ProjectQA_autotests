from xxlimited_35 import Null


def test_user_registration(register_user):
    user_data = register_user

    assert user_data["email_sent"] == user_data["email_received"]
    assert user_data["user_id"] is not None
    assert user_data["access_token"] is not None


def test_user_login(login_user, register_user):
    login_data = login_user
    user_data = register_user

    assert login_data["access_token"] is not None, "Токен пустой"
    assert len(login_data["access_token"]) > 10
    assert login_data["user_id"] == user_data["user_id"]
