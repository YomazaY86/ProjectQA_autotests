import faker
import pytest
import requests
from faker import Faker


@pytest.fixture(scope="session")
def api_client():
    return "http://localhost:8081"

@pytest.fixture(scope="session")
def faker_gen():
    fake = Faker("ru_RU")
    return fake

@pytest.fixture(scope="function")
def register_user(api_client, faker_gen):
    fake_email = faker_gen.email()
    fake_name = faker_gen.first_name_male()
    fake_password = faker_gen.password(special_chars=True, length=8, digits=True)


    new_user = requests.post(
        url=f"{api_client}/v1/users/register",
        headers={"Content-Type": "application/json"},
        json={"email": fake_email,
              "password": fake_password,
              "name": fake_name})

    assert new_user.status_code == 200, f"Регистрация неуспешна, код ответа {new_user.status_code}"
    data = new_user.json()

    print(f"Создан новый пользователь с email - {fake_email}, паролем - {fake_password}, именем - {fake_name}")

    return {"email_sent": fake_email,
            "email_received": data["user"]["email"],
            "user_id": data["user"]["id"],
            "access_token": data['accessToken']
            }

