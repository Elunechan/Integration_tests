import allure
import pytest
from components.grid_table import GridTable
from components.label_dropdown import LabeledDropdown


@allure.suite("Проверка портала под участковым")
@allure.sub_suite("Реестр запросов идентификаций")
@pytest.mark.form_key("ident") #Передаем форму которую хотим открыть
@pytest.mark.user_type("inspector") #Берем юзера из словаря, под ним проходим тест
@allure.title("Фильтрация по поднадзорному лицу")
def test_filter_inspector_for_ident(current_page):
    with allure.step("Открываем фильтр по label и дожидаемся загрузки значений"):
        dropdown = LabeledDropdown(current_page, label_text="Поднадзорное лицо")
        dropdown.open()

    with allure.step("Выбираем значение в фильтре"):
        dropdown.select_value("1010")

    with allure.step("Дожидаемся фильтрации по таблице"):
        table = GridTable(current_page)
        table.wait_loader_disappear() # Дожидаемся исчезновения лоадера

    with allure.step("Проверяем, что таблица отфильтрована по выбранному значению"):
        table.assert_column_values(col_id="column_1", expected_value="1010", )

@allure.suite("Проверка портала под участковым")
@allure.sub_suite("Реестр запросов идентификаций")
@pytest.mark.form_key("ident") #Передаем форму которую хотим открыть
@pytest.mark.user_type("inspector") #Берем юзера из словаря, под ним проходим тест
@allure.title("Фильтрация по статусу идентификации")
def test_filter_inspector_for_ident_filter(current_page):
    with allure.step("Открываем фильтр по label и дожидаемся загрузки значений"):
        dropdown = LabeledDropdown(current_page, label_text="Статус идентификации")
        dropdown.open()

    with allure.step("Выбираем значение в фильтре"):
        dropdown.select_value("Идентификация не пройдена")

    with allure.step("Дожидаемся фильтрации по таблице"):
        table = GridTable(current_page)
        table.wait_loader_disappear()  # Дожидаемся исчезновения лоадера

    with allure.step("Проверяем, что таблица отфильтрована по выбранному значению"):
        table.assert_column_values(col_id="column_8", expected_value="Идентификация не пройдена")

@allure.suite("Проверка портала под увд")
@allure.sub_suite("Реестр запросов идентификаций")
@pytest.mark.form_key("ident")
@pytest.mark.user_type("head_of_region_uvd")
@allure.title("Фильтрация по участковому")
def test_filter_inspector_ident(current_page):
    with allure.step("Открываем фильтр по label и дожидаемся загрузки значений"):
        dropdown = LabeledDropdown(current_page, label_text="Участковый")
        dropdown.open()

    with allure.step("Выбираем значение в фильтре"):
        dropdown.select_value("Участковый 001")

    with allure.step("Дожидаемся фильтрации по таблице"):
        table = GridTable(current_page)
        table.wait_loader_disappear()

    with allure.step("Проверяем, что таблица отфильтрована по выбранному значению"):
        table.scroll_to_column_header("column_13")  # <-- скроллим к нужной колонке
        table.assert_column_values(col_id="column_13", expected_value="Участковый 001")