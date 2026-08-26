def test_user_registration(register_user):
    user_data = register_user

    assert user_data["email_sent"] == user_data["email_received"]
    assert user_data["user_id"] is not None
    assert user_data["access_token"] is not None