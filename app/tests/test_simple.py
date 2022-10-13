from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_get_hello():
    response = client.get("/hello", headers={"accept": "application/json"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello!"}


# TODO(besteady): add other tests

# def test_read_item_bad_token():
#     response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


# def test_read_inexistent_item():
#     response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}


# def test_create_item():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": "foobar",
#         "title": "Foo Bar",
#         "description": "The Foo Barters",
#     }


# def test_create_item_bad_token():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "hailhydra"},
#         json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


# def test_create_existing_item():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={
#             "id": "foo",
#             "title": "The Foo ID Stealers",
#             "description": "There goes my stealer",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Item already exists"}
