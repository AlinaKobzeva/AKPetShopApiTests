from http.client import responses

import allure
import requests
import jsonschema
from .shemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, ("Код ответа не совпал с ожидаемым")

        with allure.step("Проверка текстового содерж ответа"):
            assert response.text == "Pet deleted", ("Текст ошибки не совпал с ожид")

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }

            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, ("Код ответа не совпал с ожидаемым")

        with allure.step("Проверка текстового содерж ответа"):
            assert response.text == "Pet not found", ("Текст ошибки не совпал с ожид")

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, ("Код ответа совпал с ожидаемым")

        with allure.step("Проверка текстового содерж ответа"):
            assert response.text == "Pet not found", ("Текст ошибки совпал с ожид")

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id":1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация Json-схемы"):
            assert response.status_code == 200, ("Код ответа не совпал с ожидаемым")
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload["status"], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_complete_add_pet(self):
        with allure.step("Подготовка данных для добавления питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"}

        with allure.step("Отправка запроса на добавление питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация Json-схемы"):
            assert response.status_code == 200, ("Код ответа не совпал с ожидаемым")
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload["status"], "status питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload["category"], "category питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload["photoUrls"], "photoUrls питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload["tags"], "tags питомца не совпадает с ожидаемым"


    @allure.title("Получение информации о питомце по id")
    def test_get_pet_by_id(self,create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet

        with allure.step("Отправка запроса на получение информации о питомце по Id"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json() ["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_updated_pet(self, create_pet):

        with allure.step("Подготовка обновленных данных"):
            pet_id = create_pet
            new_payload = {
                "id":  pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
        with allure.step("Отправка запроса на обновление питомца"):
           response=requests.put(f"{BASE_URL}/pet/", json=new_payload)
           assert response.status_code == 200, f"Ошибка обновления питомца: статус-код {response.status_code}"

        with allure.step("Проверка наличия обновленных данных"):
            response_get = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response_get.status_code == 200, f"Ошибка получения информации о питомце: статус-код {response_get.status_code}"

            data = response_get.json()
            assert data["name"] == "Buddy Updated", f"Имя питомца не обновилось: {data['name']} вместо Buddy Updated"
            assert data["status"] == "sold", f"Статус питомца не обновился: {data['status']} вместо sold"

    @allure.title("Удаление питомца по ID")
    def test_create_and_delete_pet(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet
        with allure.step("Удаление питомца"):
            delete_response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
            assert delete_response.status_code == 200

        with allure.step("Проверка удаления питомца"):
            get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert get_response.status_code == 404