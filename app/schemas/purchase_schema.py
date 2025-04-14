from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderSchema(BaseModel):
    order_id: Optional[int] = None
    user_id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    ordered_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "user_id": 1,
                "product_id": 1,
                "product_name": "کروسان",
                "quantity": 2,
                "ordered_at": "2025-04-14T11:30:00"
            }
        }