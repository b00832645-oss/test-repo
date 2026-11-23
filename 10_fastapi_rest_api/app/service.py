from .events import EventBus
from .models import Item, ItemIn
from .repository import ItemRepository


class ItemNotFound(Exception):
    pass


class ItemService:
    """Business rules only: no HTTP, no storage details."""

    def __init__(self, repo: ItemRepository, bus: EventBus | None = None):
        self.repo = repo
        self.bus = bus or EventBus()

    def create(self, data: ItemIn) -> Item:
        if any(i.name.lower() == data.name.lower() for i in self.repo.list()):
            raise ValueError(f"An item named '{data.name}' already exists")
        item = self.repo.add(data)
        self.bus.publish("ItemCreated", item.model_dump())
        return item

    def get(self, item_id: int) -> Item:
        item = self.repo.get(item_id)
        if item is None:
            raise ItemNotFound(item_id)
        return item

    def list(self, max_price: float | None = None) -> list[Item]:
        items = self.repo.list()
        return [i for i in items if max_price is None or i.price <= max_price]

    def update(self, item_id: int, data: ItemIn) -> Item:
        item = self.repo.update(item_id, data)
        if item is None:
            raise ItemNotFound(item_id)
        return item

    def delete(self, item_id: int) -> None:
        if not self.repo.delete(item_id):
            raise ItemNotFound(item_id)
