import logging
import pytest


# В корневой conftest.py выносить только те фикстукры, которые могут быть использованы в UI и API тестах, иначе использовать conftest непосредствоо в папке ui/api

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("autotests")

@pytest.fixture # Фикстура для логирования, можно использовать в api и ui тестах
def log_response():
    def _log_response(response):
        logger.info(f"RESPONSE: {response.status_code} {response.text}")
        return response
    return _log_response