import requests
import pytest
import allure
from helpers import generate_order_payload, cancel_order_by_track
from test_data import BASE_URL

@allure.epic("Заказ")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @allure.description(
        "Проверяем, что заказ можно создать:\n"
        "- с одним цветом (BLACK или GREY)\n"
        "- с двумя цветами (BLACK и GREY)\n"
        "- без указания цвета"
    )
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_various_colors(self, color):
        payload = generate_order_payload(color=color)
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

        track = response.json().get("track")
        cancel_order_by_track(track)

    @allure.title("Ответ при создании заказа содержит track")
    @allure.description("Проверяем, что успешный ответ на создание заказа содержит поле track")
    def test_create_order_response_contains_track(self):
        payload = generate_order_payload()
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201
        assert "track" in response.json()
        
        track = response.json().get("track")
        cancel_order_by_track(track)