from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    name: str
    price: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "کروسان",
                "price": 90000,
                "image_url": "http://example.com/product/croissant1.webp",
                "created_at": "2025-04-14T11:30:00"
            }
        }