import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


from app.main import app

client = TestClient(app)

from app.db.file_manager import fileManager

def getDb():
    return fileManager

from app.crud import crud_device

fake_db = [
    {"id": "device08",
     "crane_id": "crane2",
      "s_n": "5234934892",
      "model": "hawkeye 5",
      "description": "some description", 
      "created": "22/07/2021 06:21:19",
      "updated": "22/07/2021 08:42:59",
      "deleted": "true"},
      {"id": "device06",
      "crane_id": "crane102",
      "s_n": "5234934891", 
      "model": "hawkeye 5",
      "description": "That\u2019s a great device 5",
      "created": "22/07/2021 06:22:29",
      "updated": "22/07/2021 06:22:29",
      "deleted": "false"},
      {"id": "device12",
      "crane_id": "crane 107",
      "s_n": "5234934401",
      "model": "oregon",
      "description": "That\u2019s a great device 12",
      "created": "22/07/2021 06:32:06",
      "updated": "22/07/2021 06:37:17",
      "deleted": "false"},
      {"id": "device23",
      "crane_id": "crane1",
      "s_n": "5234934111",
      "model": "hawkeye 5",
      "description": "some description",
      "created": "22/07/2021 08:16:31",
      "updated": "22/07/2021 08:45:22",
      "deleted": "false"}
      ]

@pytest.mark.asyncio
async def test_read_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    # response = client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_devices():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/devices")
    # response = client.get("/devices")
    assert response.status_code == 200
    actual = response.json()
    expected = await crud_device.get_all_devices(getDb(), deleted=False)
    assert len(actual) == len(expected)
    assert all([(a.get('id') == b.get('id')) for a, b in zip(actual, expected)])
    assert all([(a.get('deleted') == 'false') for a in expected])


@pytest.mark.asyncio
async def test_post_device():
    id = 'device99'
    crane_id = 'crane1'
    s_n = '123456789'
    model = 'hawkeye 7'
    description = "Thats a great device"

    #region test add
    #TBD-for now need to be updated each time to run- uncomment test with new params
    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     response = await ac.post(
    #         '/devices',
    #         params=[('id',id),('crane_id',crane_id),('s_n',s_n),('model',model),('description', description)]
    #         )
    # assert response.status_code == 200
    # assert response.json() == {'msg':'device was addeed succesfully'}
    #endregion test add

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            '/devices',
            params=[('id',id),('crane_id',crane_id),('s_n',s_n),('model',model),('description', description)]
            )

    assert response.status_code == 200
    assert response.json() == {'msg':'device was updated succesfully'}

    #validate cran exist
    crane_id = 'crane_400'
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f'devices?id={id}&crane_id={crane_id}&s_n={s_n}&model={model}&description={description}'
            )
    assert response.status_code == 400
    assert response.json() == {'detail':'this crane doesnt exist'}

    #validate duplicate
    model = 'hawkeye 6'
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f'devices?id={id}&crane_id={crane_id}&s_n={s_n}&model={model}&description={description}'
            )
    assert response.status_code == 409
    assert response.json() == {'detail':'device already exists'}


@pytest.mark.asyncio
async def test_get_device():
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/devices/device99000000")
    assert response.status_code == 404

    expected = await crud_device.get_device("device99")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/devices/device99")
    assert response.status_code == 200
    assert response.json() == expected

@pytest.mark.asyncio
async def test_delete_device():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/devices/device99")
    assert response.status_code == 200
    assert response.json() == {'msg':'device has been deleted succesfully'}

@pytest.mark.asyncio
async def test_get_deleted_devices():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/devices/deleted")
    assert response.status_code == 200
    actual = response.json()
    expected = await crud_device.get_all_devices(getDb(), deleted=True)
    assert len(actual) == len(expected)
    assert all([(a.get('id') == b.get('id')) for a, b in zip(actual, expected)])
    assert all([(a.get('deleted') == 'true') for a in expected])

@pytest.mark.asyncio
async def test_restore_device():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/device/deleted/device99/restore")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_put_device():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/devices/device99?crane_id=crane2")
    assert response.status_code == 200
    assert response.json() == {'msg':'devices data updated'}