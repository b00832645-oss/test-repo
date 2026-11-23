from fastapi import APIRouter, Depends, HTTPException, status

from .events import EventBus
from .models import Item, ItemIn
from .repository import InMemoryItemRepository, ItemRepository
from .service import ItemNotFound, ItemService

router = APIRouter()

_repo = InMemoryItemRepository()
_bus = EventBus()
_bus.subscribe("ItemCreated", lambda payload: print(f"[event] new item: {payload['name']}"))


def get_repository() -> ItemRepository:
    return _repo


def get_service(repo: ItemRepository = Depends(get_repository)) -> ItemService:
    return ItemService(repo, _bus)


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items", response_model=list[Item])
def list_items(max_price: float | None = None, service: ItemService = Depends(get_service)):
    return service.list(max_price)


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemIn, service: ItemService = Depends(get_service)):
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, service: ItemService = Depends(get_service)):
    try:
        return service.get(item_id)
    except ItemNotFound:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, data: ItemIn, service: ItemService = Depends(get_service)):
    try:
        return service.update(item_id, data)
    except ItemNotFound:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ItemService = Depends(get_service)):
    try:
        service.delete(item_id)
    except ItemNotFound:
        raise HTTPException(status_code=404, detail="Item not found")
