import allure
import pytest
import requests
import jsonschema

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_store_order(self):
        with allure.step("Подготовка данных дл отправки"):
            payload = {
                "id":1,
                "petID": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)
            assert response.status_code == 200, f'Ожидался код статуса 200, но получен {response.status_code}'
            with allure.step('Проверка содержимого ответа'):
                response.json()
