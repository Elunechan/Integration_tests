from datetime import datetime

import pytest
import allure
from playwright.sync_api import Page, expect
from configs.env import USERS, FORMS
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def current_page(login_page: LoginPage, request) -> Page:
    """Авторизация и переход на нужную форму"""
    form_key_marker = request.node.get_closest_marker("form_key")
    user_type_marker = request.node.get_closest_marker("user_type")

    form_key = form_key_marker.args[0] if form_key_marker else "users"
    user_type = user_type_marker.args[0] if user_type_marker else "inspector"

    login_page.page.goto(FORMS["users"])  # Переход на базовую страницу с логином
    login_page.login(
        USERS[user_type]["login"],
        USERS[user_type]["password"]
    )

    login_page.page.goto(FORMS[form_key])  # Переход уже после логина
    expect(login_page.page).to_have_url(FORMS[form_key])  # Проверка перехода

    return login_page.page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Скриншот при падении теста"""
    outcome = yield
    report = outcome.get_result()

    if report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG
        )

@pytest.fixture
def today_date():
    """
    Фикстура, возвращающая сегодняшнюю дату в формате ДД.ММ.ГГГГ.
    """
    return datetime.today().strftime("%d.%m.%Y")