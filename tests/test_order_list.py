import requests
import allure
from test_data import BASE_URL
from helpers import generate_order_payload, cancel_order_by_track

@allure.epic("Заказ")
@allure.feature("Список заказов")
class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    @allure.description("Проверяем, что при запросе /orders возвращается список заказов в теле ответа")
    def test_get_orders_list(self):
        payload = generate_order_payload()
        create_response = requests.post(f"{BASE_URL}/orders", json=payload)

        response = requests.get(f"{BASE_URL}/orders")
        body = response.json()

        assert "orders" in body
        assert isinstance(body["orders"], list)

        track = create_response.json().get("track")
        cancel_order_by_track(track)

