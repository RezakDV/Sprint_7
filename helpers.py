import requests
import random
import string
from datetime import datetime, timedelta
from faker import Faker
from test_data import BASE_URL

def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/courier", data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

def generate_order_payload(color=None):
    faker = Faker("ru_RU")
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "address": faker.address(),
        "metroStation": random.randint(1, 10),
        "phone": faker.phone_number(),
        "rentTime": random.randint(1, 10),
        "deliveryDate": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "comment": faker.sentence(nb_words=5),
        "color": color or []
    }

def login_courier(login: str, password: str):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/courier/login", json=payload)
    return response

def delete_courier_by_id(courier_id: int):
    response = requests.delete(f"{BASE_URL}/courier/{courier_id}", json={"id": str(courier_id)})
    return response

def cancel_order_by_track(track: int):
    response = requests.put(f"{BASE_URL}/orders/cancel", json={"track": track})
    return response
