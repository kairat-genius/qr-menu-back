from ...API.ResponseModels.Register import RegisterResponseFail
from ...API.ResponseModels.Restaurant import RestaurantData

from .func import (get_restaurant, get_restaurant_update, 
                   delete_resturant, register_restaurant)
from ..User.func import registration, delete_user
from ..User import users

from ...settings import COOKIE_KEY
import pytest, pytest_asyncio
import httpx


@pytest_asyncio.fixture(scope="module", params=users)
async def setup_user(client: httpx.AsyncClient, request):
    data = request.param

    status, user, token = await registration(client, data)

    assert status == 200 and RegisterResponseFail(**user)

    yield token

@pytest.mark.asyncio
async def test_register_restaurant_fail_cookie(client: httpx.AsyncClient):
    status, data = await register_restaurant(client, None, None)

    assert status == 401 and ("detail" in data) is True


@pytest.mark.asyncio
async def test_restaurant_update_fail(client: httpx.AsyncClient):
    request = await client.patch('/api/admin/update/restaurant')

    assert request.status_code == 401 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_get_fail(client: httpx.AsyncClient):
    request = await client.get('/api/admin/get/restaurant')

    assert request.status_code == 401 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_delete_fail(client: httpx.AsyncClient):
    status, data = await delete_resturant(client, None, cookies=False)

    assert status == 401 and ("detail" in data) is True

@pytest.mark.asyncio
async def test_restaurant_data_delete_fail(client: httpx.AsyncClient):
    request = await client.patch("/api/admin/delete/data")

    assert request.status_code == 401 

@pytest.mark.asyncio
async def test_get_full_info_fail(client: httpx.AsyncClient):
    request = await client.get('/api/admin/get-full-info/restaurant')

    assert request.status_code == 401 and ("detail" in request.json()) is True


@pytest.mark.asyncio
async def test_register_restaurant(client: httpx.AsyncClient, setup_user: str):
    status, data = await register_restaurant(client, get_restaurant(), setup_user)

    assert status == 200 and RestaurantData(**data)


@pytest.mark.asyncio
async def test_register_restaurant_already_exists(client: httpx.AsyncClient, setup_user: str):
    status, _ = await register_restaurant(client, get_restaurant(), setup_user)

    assert status == 423


@pytest.mark.asyncio
async def test_restaurant_update(client: httpx.AsyncClient, setup_user: str):
    cookie = {COOKIE_KEY: setup_user}
    
    request = await client.patch('/api/admin/update/restaurant',
                          cookies=cookie, json=get_restaurant_update())

    update = request.json()
    assert (update == get_restaurant() | {"address": "st. Example, 202", "start_day": "Monday", 
                                         "end_day": "Friday", "start_time": "9:00", 
                                         "end_time": "21:00", "id": update.get("id")}) is True
    
    assert request.status_code == 200 and RestaurantData(**update)


@pytest.mark.asyncio
async def test_get_full_info(client: httpx.AsyncClient, setup_user: str):
    cookie = {COOKIE_KEY: setup_user}

    request = await client.get('/api/admin/get-full-info/restaurant', cookies=cookie)

    assert request.status_code == 200


@pytest.mark.asyncio
async def test_restaurant_get(client: httpx.AsyncClient, setup_user: str):
    cookie = {COOKIE_KEY: setup_user}

    request = await client.get('/api/admin/get/restaurant', cookies=cookie)

    assert request.status_code == 200 and RestaurantData(**request.json())


@pytest.mark.asyncio
async def test_restaurant_data_delete(client: httpx.AsyncClient, setup_user: str):
    cookie = {COOKIE_KEY: setup_user}

    request = await client.patch("/api/admin/delete/data", cookies=cookie,
                                 json={"start_day": True, "start_time": True})

    data = request.json()

    assert (data == get_restaurant() | {"address": "st. Example, 202", "start_day": None, 
                                         "end_day": "Friday", "start_time": None, 
                                         "end_time": "21:00", "id": data.get("id")}) is True
    
    assert request.status_code == 200 and RestaurantData(**data)


@pytest.mark.asyncio
async def test_restaurant_delete(client: httpx.AsyncClient, setup_user: str):
    status, data = await delete_resturant(client, setup_user)

    assert status == 200 and ("msg" in data) is True