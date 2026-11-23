from abc import ABC, abstractmethod
from itertools import count

from .models import Item, ItemIn


class ItemRepository(ABC):
    """Abstraction the service depends on (Dependency Inversion)."""

    @abstractmethod
    def add(self, data: ItemIn) -> Item: ...

    @abstractmethod
    def get(self, item_id: int) -> Item | None: ...

    @abstractmethod
    def list(self) -> list[Item]: ...

    @abstractmethod
    def update(self, item_id: int, data: ItemIn) -> Item | None: ...

    @abstractmethod
    def delete(self, item_id: int) -> bool: ...


class InMemoryItemRepository(ItemRepository):
    """Simple implementation; a SQLAlchemy version would implement the same interface."""

    def __init__(self):
        self._items: dict[int, Item] = {}
        self._ids = count(1)

    def add(self, data: ItemIn) -> Item:
        item = Item(id=next(self._ids), **data.model_dump())
        self._items[item.id] = item
        return item

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def list(self) -> list[Item]:
        return list(self._items.values())

    def update(self, item_id: int, data: ItemIn) -> Item | None:
        if item_id not in self._items:
            return None
        self._items[item_id] = Item(id=item_id, **data.model_dump())
        return self._items[item_id]

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None
