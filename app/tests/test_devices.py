from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

from app.api.file_manager import fileManager
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

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_delete_device():
    response = client.delete("/devices/device08")
    assert response.status_code == 200
    assert response.json() == {'msg':'device has been deleted succesfully'}

def test_get_deleted_devices():
    response = client.get("/devices/deleted")
    assert response.status_code == 200
    actual = response.json()
    expected = crud_device.get_all_devices(getDb(), deleted=True)
    assert len(actual) == len(expected)
    assert all([(a.get('id') == b.get('id')) for a, b in zip(actual, expected)])
    assert all([(a.get('deleted') == 'true') for a in expected])

def test_get_devices():
    response = client.get("/devices")
    assert response.status_code == 200
    actual = response.json()
    expected = crud_device.get_all_devices(getDb(), deleted=False)
    assert len(actual) == len(expected)
    assert all([(a.get('id') == b.get('id')) for a, b in zip(actual, expected)])
    assert all([(a.get('deleted') == 'false') for a in expected])

def test_get_device():
    response = client.get("/devices/device02")
    assert response.status_code == 404

    expected = crud_device.get_device("device23")
    response = client.get("/devices/device23")
    assert response.status_code == 200
    assert response.json() == expected

def test_post_device():
    response = client.post(
            'devices?id=device03&crane_id=crane1&s_n=5234934890&model=hawkeye%205&description=That%E2%80%99s%20a%20great%20device',
        )
    assert response.status_code == 200
    assert response.json() == {'msg':'device was updated succesfully'}
    response = client.post(
            'devices?id=device03&crane_id=crane101&s_n=523493482&model=hawkeye%205&description=That%E2%80%99s%20a%20great%20device',
        )
    assert response.status_code == 409
    assert response.json() == {'detail':'device already exists'}


    #region test add
    #TBD-for now need to be updated each time to run- uncomment test with new params
    # id ="device05"
    # s_n = "5234934890"
    # response = client.post(
    #         '/devices?id=' + id + '&crane_id="crane101"&' + s_n +'=&model="hawkeye 5"&description="That’s a great device"',
    #     )
    # assert response.status_code == 200
    # assert response.json() == {'msg':'device was addeed succesfully'}
    #endregion test add


    #validate cran exist
    response = client.post(
            '/devices?id="device08"&crane_id="crane101"&s_n="5234934892"&model="hawkeye 5"&description="That’s a great device"',
        )
    assert response.status_code == 404
    assert response.json() == {'detail':'this crane doesnt exist'}

def test_put_device():
    response = client.put("/devices/device08?crane_id=crane2")
    assert response.status_code == 200
    assert response.json() == {'msg':'devices data updated'}

def test_restore_device():
    response = client.post("/device/deleted/device08/restore")
    assert response.status_code == 200