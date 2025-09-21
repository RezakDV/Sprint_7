import requests
import pytest
import allure
from helpers import generate_random_string, register_new_courier_and_return_login_password, delete_courier_by_id
from test_data import BASE_URL

@allure.epic("Курьер")
@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться")
    @allure.description("Курьер может авторизоваться при передаче корректных login и password. Успешный запрос возвращает id.")
    def test_login_courier_success(self):
        creds = register_new_courier_and_return_login_password()
        payload = {
            "login": creds[0],
            "password": creds[1]
        }

        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 200
        assert "id" in response.json()

        delete_courier_by_id(response.json()["id"])

    @allure.title("Авторизация требует обязательные поля")
    @allure.description("Если login или password не переданы, система возвращает ошибку 400 с сообщением 'Недостаточно данных для входа'.")
    # В эндпоинте обнаружен баг: при отсутствии password возвращается 504 вместо 400
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_required_field(self, missing_field):
        creds = register_new_courier_and_return_login_password()
        payload = {
            "login": creds[0],
            "password": creds[1]
        }

        payload.pop(missing_field)

        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json()["message"]

    @allure.title("Ошибка при неверном логине или пароле")
    @allure.description("Если указать неправильный login или password, система возвращает ошибку 404 с сообщением 'Учетная запись не найдена'.")
    @pytest.mark.parametrize("field, value", [
        ("login", "wrong_login"),
        ("password", "wrong_password")
    ])
    def test_login_courier_invalid_credentials(self, field, value):
        creds = register_new_courier_and_return_login_password()
        payload = {
            "login": creds[0],
            "password": creds[1]
        }

        payload[field] = value

        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Ошибка при авторизации несуществующего курьера")
    @allure.description("Если авторизоваться под несуществующим пользователем, система возвращает ошибку 404 с сообщением 'Учетная запись не найдена'.")
    def test_login_courier_nonexistent_user(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }

        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
