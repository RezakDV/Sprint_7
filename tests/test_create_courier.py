import requests
import pytest
import allure
from helpers import generate_random_string, register_new_courier_and_return_login_password, delete_courier_by_id, login_courier
from test_data import BASE_URL

@allure.epic("Курьер")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    @allure.description("Проверяем, что курьера можно создать при передаче всех обязательных полей")
    def test_create_courier_success(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 201
        assert response.json()["ok"] is True

        delete_courier_by_id(login_courier(payload["login"], payload["password"]).json().get("id"))

    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description("Проверяем, что повторная регистрация с теми же данными вызывает ошибку 409")
    def test_create_courier_duplicate(self):
        creds = register_new_courier_and_return_login_password()
        payload = {
            "login": creds[0],
            "password": creds[1],
            "firstName": creds[2]
        }

        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

        delete_courier_by_id(login_courier(payload["login"], payload["password"]).json().get("id"))
    
    @allure.title("Создание курьера с обязательными полями")
    @allure.description("Проверяем, что для создания курьера достаточно передать login и password")
    # В соответствии с документацией, firstName — необязательное поле
    def test_create_courier_required_fields(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
        }

        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 201
        assert response.json()["ok"] is True

        delete_courier_by_id(login_courier(payload["login"], payload["password"]).json().get("id"))

    @allure.title("Ошибка при отсутствии обязательного поля")
    @allure.description("Проверяем, что если одного из обязательных полей нет, возвращается ошибка 400")
    # В соответствии с документацией, firstName — необязательное поле
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
        }

        payload.pop(missing_field)
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json()["message"]

    @allure.title("Ошибка при создании курьера с занятым логином")
    @allure.description("Проверяем, что при создании курьера с уже существующим логином возвращается ошибка 409")
    def test_create_courier_existing_login(self):
        creds = register_new_courier_and_return_login_password()
        payload = {
            "login": creds[0],
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]
