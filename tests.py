from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    response = client.post(url="http://127.0.0.1:8000/create",
                           json=
                           {
                               "id": "12345678123456781234567812345678",
                               "create_ad": "2002-09-10",
                               "login": "superuser",
                               "password": "kill",
                               "project_id": "87654321876543218765432187654321",
                               "env": "stage",
                               "domain": "regular"
                           })
    assert response.status_code == 200
    assert response.json() == "Created user superuser"


def test_create_double_user():
    response = client.post(url="http://127.0.0.1:8000/create",
                           json=
                           {
                               "id": "12345678123456781234567812345678",
                               "create_ad": "2002-09-10",
                               "login": "superuser",
                               "password": "kill",
                               "project_id": "87654321876543218765432187654321",
                               "env": "stage",
                               "domain": "regular"
                           })
    assert response.status_code == 200
    assert response.json() == "User with id 12345678-1234-5678-1234-567812345678 already exists"


def test_create_bad_user():
    response = client.post(url="http://127.0.0.1:8000/create",
                           json=
                           {
                               "id": "111",
                               "create_ad": "2002-09-10",
                               "login": "superuser",
                               "password": "kill",
                               "project_id": "222",
                               "env": "stage",
                               "domain": "regular"
                           })
    assert response.status_code == 422


def test_get_all_users():
    response = client.get(url="http://127.0.0.1:8000/get_users")
    assert response.status_code == 200
    assert response.json()


def test_get_all_users_wrong():
    response = client.post(url="http://127.0.0.1:8000/get_users")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_lock_user():
    response = client.put(url="http://127.0.0.1:8000/lock/12345678123456781234567812345678")
    assert response.status_code == 200
    assert response.json() == 'User 12345678-1234-5678-1234-567812345678 is locked now'


def test_unlock_user():
    response = client.put(url="http://127.0.0.1:8000/unlock/12345678123456781234567812345678")
    assert response.status_code == 200
    assert response.json() == 'User 12345678-1234-5678-1234-567812345678 is no longer locked'


def test_unlock_user_second_time():
    response = client.put(url="http://127.0.0.1:8000/unlock/12345678123456781234567812345678")
    assert response.status_code == 200
    assert response.json() == 'User 12345678-1234-5678-1234-567812345678 is not locked now'
