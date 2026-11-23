import pytest
from fastapi.testclient import TestClient

from app.api import get_repository
from app.events import EventBus
from app.main import app
from app.models import ItemIn
from app.repository import InMemoryItemRepository
from app.service import ItemNotFound, ItemService


@pytest.fixture
def client():
    repo = InMemoryItemRepository()                       # fresh storage for each test
    app.dependency_overrides[get_repository] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_root(client):
    assert client.get("/").json() == {"Hello": "World"}


def test_create_and_read_item(client):
    created = client.post("/items", json={"name": "Mug", "price": 12.0})
    assert created.status_code == 201
    item_id = created.json()["id"]
    assert client.get(f"/items/{item_id}").json() == {"id": item_id, "name": "Mug", "price": 12.0, "in_stock": True}


@pytest.mark.parametrize("body", [{"name": "", "price": 1}, {"name": "X", "price": -3}, {"price": 5}])
def test_invalid_body_is_rejected_with_422(client, body):
    assert client.post("/items", json=body).status_code == 422


def test_duplicate_name_conflict(client):
    client.post("/items", json={"name": "Mug", "price": 12})
    assert client.post("/items", json={"name": "mug", "price": 9}).status_code == 409


def test_list_filter_update_delete(client):
    client.post("/items", json={"name": "Mug", "price": 12})
    client.post("/items", json={"name": "Hat", "price": 30})
    assert [i["name"] for i in client.get("/items", params={"max_price": 20}).json()] == ["Mug"]
    assert client.put("/items/2", json={"name": "Cap", "price": 18}).json()["name"] == "Cap"
    assert client.delete("/items/1").status_code == 204
    assert client.get("/items/1").status_code == 404


def test_unknown_item_404(client):
    assert client.put("/items/99", json={"name": "X", "price": 1}).status_code == 404
    assert client.delete("/items/99").status_code == 404


# ---- service tested without HTTP: the benefit of the layered design ---------------
def test_service_publishes_event_on_create():
    bus = EventBus()
    received = []
    bus.subscribe("ItemCreated", received.append)
    ItemService(InMemoryItemRepository(), bus).create(ItemIn(name="Lamp", price=40))
    assert received == [{"id": 1, "name": "Lamp", "price": 40.0, "in_stock": True}]


def test_service_raises_for_missing_item():
    with pytest.raises(ItemNotFound):
        ItemService(InMemoryItemRepository()).get(1)
