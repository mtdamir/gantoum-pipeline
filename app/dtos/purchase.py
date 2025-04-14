from pydantic import BaseModel
from typing import List

class OrderItemDto(BaseModel):
    product_name: str  
    quantity: int


class CreateOrderDto(BaseModel):
    items: List[OrderItemDto]

