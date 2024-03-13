from app.API.ResponseModels.Register import RegisterResponseFail
from app.API.ResponseModels.Register import RegisterUserData

from .func import (login, login_by_token,
                   registration)
from . import users

from ...settings import COOKIE_KEY
import pytest
import pytest_asyncio
import httpx


@pytest_asyncio.fixture(scope="module", params=users)
async def register(client: httpx.AsyncClient, request):
    user = request.param

    status, response, token = await registration(client, user)

    assert status == 200 and RegisterResponseFail(**response)

    yield token, user

@pytest.mark.asyncio
async def test_register_already_exists(client: httpx.AsyncClient, register: tuple, event_loop):
    _, user  = register

    status, _, _ = await registration(client, user)

    assert status == 403 

@pytest.mark.asyncio
async def test_login_by_token_fail(client: httpx.AsyncClient, event_loop):
    status, _ = await login_by_token(client, "oueqwbfuoeqb")

    assert status == 401

@pytest.mark.asyncio
async def test_login_by_token_success(client: httpx.AsyncClient, register: str, event_loop):
    status, data = await login_by_token(client, register[0])
    
    assert status == 200 and RegisterUserData(**data)

@pytest.mark.asyncio
async def test_delete_user_session(client: httpx.AsyncClient, register: str, event_loop):
    cookie = {COOKIE_KEY: register[0]}

    request = await client.delete('/api/admin/delete/session/user',
                            cookies=cookie)
    
    assert request.status_code == 200


@pytest.mark.asyncio
async def test_login_success(client: httpx.AsyncClient, register: tuple, event_loop):
    status, user, _ = await login(client, register[1])

    assert status == 200 and RegisterResponseFail(**user)

@pytest.mark.asyncio
async def test_login_fail(client: httpx.AsyncClient, register: tuple, event_loop):
    data = register[1]

    data['password'] = "".join([chr(ord(i) + 2) for i in data["password"]])

    status, response, _ =  await login(client, data)

    msg: str = response.get("detail")

    assert status == 403 and msg.startswith("Хибний пароль") is True


@pytest.mark.asyncio
async def test_register_invalid_data(client: httpx.AsyncClient, register: tuple, event_loop):
    _, user  = register

    user.pop("password")

    status, _, _ = await registration(client, user)

    assert status == 422


@pytest.mark.asyncio
async def test_get_full_info_fail(client: httpx.AsyncClient, register: tuple, event_loop):
    cookie = {COOKIE_KEY: register[0]}

    request = await client.get('/api/admin/get-full-info/user',
                         cookies=cookie)
    
    assert request.status_code == 400

