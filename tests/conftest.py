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


@pytest.fixture(scope="session")
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
    user_id = data.get("user", {}).get("id")

    print(f"Создан новый пользователь с email - {fake_email}, паролем - {fake_password}, именем - {fake_name}")

    return {"email_sent": fake_email,
            "email_received": data["user"]["email"],
            "user_id": user_id,
            "access_token": data['accessToken'],
            "password": fake_password
            }


@pytest.fixture()
def login_user(api_client,register_user):
    user_data = register_user

    login = requests.post(url=f"{api_client}/v1/users/login",
                          headers={"Content-Type": "application/json"},
                          json={"email": user_data["email_sent"],
                                "password": user_data["password"]})

    assert login.status_code == 200, f"Логин пользователя не успешен, код ответа {login.status_code}"

    print(f"Пользователь авторизован под логином {user_data["email_sent"]} и паролем {user_data["password"]}")

    response_data = login.json()

    return {"access_token": response_data["accessToken"],
            "user_id": response_data["user"]["id"]}


@pytest.fixture()
def get_first_product_id(api_client):
    get_all_products = requests.get(url=f"{api_client}/v1/products")

    assert get_all_products.status_code == 200, f"Ошибка получения товаров код {get_all_products.status_code}"

    all_products = get_all_products.json()
    first_product = all_products["products"][0]

    return first_product["id"]










