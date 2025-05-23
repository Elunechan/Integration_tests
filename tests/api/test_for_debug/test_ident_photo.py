import allure
import requests

from configs.env import BASE_URL
from models.dictionaries_models import DictionaryValuesResponse
from utils.parse_response import parse_response

@allure.suite("Проверка ECHD_ID")
@allure.sub_suite("Справочник мониторинг лиц")
@allure.title("Поиск нужного ECHD ID")
def test_dictionary_contains_expected_id(auth_headers):
    dictionary_id = 25
    expected_id = "4665578445795394820"
    url = f"{BASE_URL}/dictionaries/v1/{dictionary_id}/values"
    params = {"attributes": "NAME"}

    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200, f"Статус-код не 200: {response.status_code}"

    data = parse_response(response, DictionaryValuesResponse)

    # Собираем все значения из elements, фильтруем None и пустые строки
    all_values = [val for el in data.elements for val in el.values if val and val.strip()]
    assert expected_id in all_values, f"ID {expected_id} не найден среди values: {all_values}"