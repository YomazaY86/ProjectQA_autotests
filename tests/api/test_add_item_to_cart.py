import requests


def test_add_item_to_cart(get_first_product_id, register_user, api_client):

    user_id = register_user["user_id"]
    authorization_token = register_user["access_token"]

    check_basket_items_before = requests.get(url=f"{api_client}/v1/users/{user_id}/cart",
                                             headers={"Authorization": f"Bearer {authorization_token}"})

    assert check_basket_items_before.status_code == 200, f"Ошибка получения корзины, код {check_basket_items_before.status_code}"

    basket_items_before = check_basket_items_before.json()
    basket_counter_before = len(basket_items_before.get("items"))
    print(f"В корзине {basket_counter_before} товаров")


    add_item = requests.post(url=f"{api_client}/v1/users/{user_id}/cart/items",
                             headers={"Authorization": f"Bearer {authorization_token}"},
                             json={"product_id": get_first_product_id,
                                   "quantity": 1})

    assert add_item.status_code == 200, "Ошибка добавления товара"

    check_basket_items_after = requests.get(url=f"{api_client}/v1/users/{user_id}/cart",
                                            headers={"Authorization": f"Bearer {authorization_token}"})

    basket_items_after = check_basket_items_after.json()
    basket_counter_after = len(basket_items_after.get("items"))
    print(f"В корзине {basket_counter_after} товаров после добавления")


    assert basket_counter_before == basket_counter_after - 1, "Ошибка добавления в корзину - товар не добавлен"
    assert get_first_product_id == basket_items_after["items"][0]["productId"], "id товаров разные"
    assert basket_counter_after == 1, "Количество товаров в корзине не равно 1"