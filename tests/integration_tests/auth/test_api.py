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


async def auth_services(ac: AsyncClient):
    register_user = await ac.post()
