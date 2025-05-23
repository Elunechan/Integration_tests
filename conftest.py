import logging
import pytest
import requests
from configs.env import BASE_AUTH_URL, realm


# В корневой conftest.py выносить только общие для UI и API фикстуры, точечные лучше разбивать по фикстурам находящимся в ui и api папках

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def log_response(response):
    logger.info(f"Response: {response.status_code} {response.text}")
    return response

@pytest.fixture
def auth_token():
    """
    Фикстура для получения токена авторизации, который можно использовать в других тестах.
    Возвращает access_token или вызывает исключение при неудачной авторизации.
    """
    try:
        # Запрос токена
        response = requests.post(
            f"{BASE_AUTH_URL}/realms/{realm}/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": "corp-engine",
                "username": "test-1",
                "password": "test-1"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        response.raise_for_status()  # Проверка HTTP-статуса
        token_data = response.json()  # Парсинг JSON
        return token_data["access_token"]

    except requests.exceptions.JSONDecodeError as e:
        pytest.fail(f"Ошибка: сервер вернул не JSON. Проверь URL и параметры запроса. Ошибка: {e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка запроса: {e}")
    except KeyError:
        pytest.fail("В ответе сервера отсутствует access_token")