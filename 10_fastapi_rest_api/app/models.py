from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    """Request body: validated automatically by FastAPI (422 if invalid)."""
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    in_stock: bool = True


class Item(ItemIn):
    """Response model: an item stored in the catalogue."""
    id: int
