from fastapi import APIRouter, Depends
from dtos.purchase import CreateOrderDto
from schemas.purchase_schema import OrderSchema
from schemas.product_schema import ProductSchema
from service.purchases_service import OrderService
from guards.user_guards import user_guard

router = APIRouter()
order_service = OrderService()

@router.post("", response_model=list[OrderSchema] | list[ProductSchema])
async def create_order(order_data: CreateOrderDto | None = None, payload: dict = Depends(user_guard)):
    user_id = payload["user_id"]
    return await order_service.create_order(user_id, order_data)

@router.get("", response_model=list[OrderSchema])
async def get_user_orders(payload: dict = Depends(user_guard)):
    user_id = payload["user_id"]
    return await order_service.get_user_orders(user_id)