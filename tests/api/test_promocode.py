import requests

def test_apply_promocode(login_user, get_first_product_id, api_client):

    user_id = login_user["user_id"]
    first_product_id = get_first_product_id
    access_token = login_user["access_token"]

    add_item = requests.post(url=f"{api_client}/v1/users/{user_id}/cart/items",
                             json={"product_id": first_product_id,
                                   "quantity": 1},
                             headers={"Authorization": f"Bearer {access_token}"})

    assert add_item.status_code == 200, f"Ошибка добавления товара в корзину, код {add_item.status_code}"
    print(f"Товар успешно добавлен в корзину")

    invalid_promo = "12345"
    valid_promo = "SAVE10"

    apply_invalid_promo_code = requests.post(url=f"{api_client}/v1/users/{user_id}/cart/promocode",
                                             json={"code": invalid_promo},
                                             headers={"Authorization": f"Bearer {access_token}"})

    assert apply_invalid_promo_code.status_code == 404, f"Не валидный код ошибки применения промо {apply_invalid_promo_code.status_code}"
    print("Успешно проверен код невалидного промо")

    apply_valid_promo_code = requests.post(url=f"{api_client}/v1/users/{user_id}/cart/promocode",
                                             json={"code": valid_promo},
                                             headers={"Authorization": f"Bearer {access_token}"})

    assert apply_valid_promo_code.status_code == 200, f"Не валидный код ошибки применения промо {apply_valid_promo_code.status_code}"
    print("Успешно проверен код валидного промо ")

    get_basket = requests.get(url=f"{api_client}/v1/users/{user_id}/cart",
                                    headers={f"Authorization": f"Bearer {access_token}"})

    assert get_basket.status_code == 200, "Ошибка получения корзины"

    data_basket = get_basket.json()

    assert data_basket["appliedPromocode"] == valid_promo, f"Поле значение поля appliedPromocode {data_basket["appliedPromocode"]}, ожидаемое значение {valid_promo}"
    assert data_basket["discountCents"] is not "", f"Скидка не применилась и = {data_basket["discountCents"]}"








