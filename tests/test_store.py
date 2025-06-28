import allure
import pytest
import requests
import jsonschema
from .shemas.store_schema import STORE_SCHEMA


from tests.shemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_post_store_order(self):
        with allure.step("Подготовка данных для отправки"):
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

    @allure.title("Получение информации о заказе по ID")
    def test_get_store_order_id(self):
            with allure.step("Отправка запроса на получение информации о заказе"):
                response = requests.get(url=f"{BASE_URL}/store/order/1")
            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 200, ("Код ответа совпал с ожидаемым")

    @allure.title("Удаление заказа по id")
    def test_delete_order_id(self):
        with allure.step("Отправка запроса на удаление заказа"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, ("Код ответа  совпал с ожидаемым")

            with allure.step("Отправка запроса на получение информации о заказе"):
                response = requests.get(url=f"{BASE_URL}/store/order/1")
            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 404, ("Код ответа совпал с ожидаемым")

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_store_order_id_nonexistent(self):
        with allure.step("Отправка запроса на получение информации о заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, ("Код ответа совпал с ожидаемым")

    @allure.title("Получение инвенторя магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение информации об инвенторе"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()
            assert response.status_code == 200, ("Код ответа  совпал с ожидаемым")
            jsonschema.validate(response_json, STORE_SCHEMA)










