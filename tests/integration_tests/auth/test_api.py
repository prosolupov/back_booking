import pytest
from httpx import AsyncClient

from src.services.auth import AuthService


def test_encode_and_decode():
    data = {"user": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().decode_access_token(jwt_token)

    assert payload
    assert payload.get("user") == data.get("user")


@pytest.mark.parametrize("email, password, status_code", [
    ("pes@kat.ru", "1234", 200),
    ("pes@kat.ru", "1234", 409),
    ("pes@kat163.ru", "1234", 200),
    ("pes@kat163.ru", "1234", 409),
])
async def test_auth_services_register(
        ac: AsyncClient,
        email: str,
        password: str,
        status_code: int,
):
    register_user = await ac.post(
        "/auth/register",
        json={
            "first_name": "Kosty",
            "last_name": "Prosolupov",
            "email": email,
            "password": password,
        }
    )

    assert register_user.status_code == status_code
    if register_user.status_code == 500:
        assert register_user.json()["detail"] == "duplicate key value 'users_email'"


@pytest.mark.parametrize("email, password, status_code", [
    ("pes@kat.ru", "1234", 200),
    ("pesik@kat.ru", "1234", 404),
    ("pes@kat163.ru", "1234", 200),
    ("pes@kat", "1234", 422),
])
async def test_auth_services_login(
        ac: AsyncClient,
        email: str,
        password: str,
        status_code: int,
):
    login_user = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )

    assert login_user.status_code == status_code

    if login_user.status_code == 404:
        assert login_user.json()["detail"] == "Пользователь не найден"

    if login_user.status_code == 200:
        assert login_user.cookies.get("access_token")


async def test_auth_services_me_and_logout(ac: AsyncClient):
    me_user = await ac.get("/auth/me")
    assert me_user.status_code == 200
    assert me_user.json()["first_name"]
    assert me_user.json()["last_name"]
    assert me_user.json()["email"]

    # logout_user = await ac.post("/auth/logout")
    # assert logout_user.status_code == 200
    # assert not logout_user.cookies.get("access_token")
    #
    # me_user_logout = await ac.post("/auth/me")
    # assert me_user_logout.status_code == 405

