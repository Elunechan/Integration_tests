import pytest
import requests
from configs.env import BASE_AUTH_URL, USERS, realm, client_id

@pytest.fixture
def auth_headers(request):
    # Пытаемся найти маркер user_type, если нет — дефолтный юзер "admin"
    user_type_marker = request.node.get_closest_marker("user_type")
    user_type = user_type_marker.args[0] if user_type_marker else "admin"
    creds = USERS.get(user_type, USERS["admin"])
    login = creds["login"]
    password = creds["password"]
    resp = requests.post(
        f"{BASE_AUTH_URL}/realms/{realm}/protocol/openid-connect/token",
        data={
            "grant_type": "password",
            "client_id": client_id,
            "username": login,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }