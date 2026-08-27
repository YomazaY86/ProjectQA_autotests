import requests


def test_get_products(api_client):
    get_products = requests.get(f"{api_client}/v1/products")

    assert get_products.status_code == 200, f"Ошибка получения списка товаров, код {get_products.status_code}"

    product_list = get_products.json()

    assert isinstance(product_list, dict), f"Тип данных товаров не является словарем, полученный тип {type(product_list)}"
    assert "products" in product_list, f"Отсутствует список products"
    assert len(product_list["products"]) != 0, f"Список products получен пустым содержание: {product_list}"
    assert "id" in product_list["products"][0], "Нет id"
    assert "name" in product_list["products"][0], "Нет name"
    assert "priceCents" in product_list["products"][0], "Нет priceCents"
    assert "brand" in product_list["products"][0], "Нет brand"
