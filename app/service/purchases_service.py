import logging
from fastapi import HTTPException
from db.create_order_table import create_order, get_orders_by_user
from db.postgres_connection import get_connection
from schemas.purchase_schema import OrderSchema
from schemas.product_schema import ProductSchema
from dtos.purchase import CreateOrderDto

logger = logging.getLogger(__name__)

class OrderService:
    async def _get_all_products(self):
        async for conn in get_connection():
            try:
                result = await conn.fetch("""
                    SELECT id, name, price, image_url, created_at
                    FROM public.products;
                """)
                return [dict(row) for row in result]
            except Exception as e:
                logger.error(f"Error fetching products: {e}")
                raise

    async def _get_product_by_name(self, product_name: str):
        async for conn in get_connection():
            try:
                result = await conn.fetchrow("""
                    SELECT id, name, price, image_url, created_at
                    FROM public.products
                    WHERE name = $1;
                """, product_name)
                return dict(result) if result else None
            except Exception as e:
                logger.error(f"Error fetching product by name: {e}")
                raise

    async def create_order(self, user_id: int, order_data: CreateOrderDto | None) -> list[OrderSchema] | list[ProductSchema]:
        if order_data is None or not order_data.items:
            products = await self._get_all_products()
            return [ProductSchema(**product) for product in products]

        orders = []
        for item in order_data.items:
            product = await self._get_product_by_name(item.product_name)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with name {item.product_name} not found")

            created_order = await create_order(user_id, product["id"], item.quantity, order_name=item.product_name)
            orders.append(
                OrderSchema(
                    order_id=created_order["order_id"],
                    order_name=created_order["order_name"],
                    user_id=created_order["user_id"],
                    product_id=created_order["product_id"],
                    product_name=product["name"],
                    quantity=created_order["quantity"],
                    ordered_at=created_order["ordered_at"]
                )
            )
        return orders

    async def get_user_orders(self, user_id: int) -> list[OrderSchema]:
        orders = await get_orders_by_user(user_id)
        return [OrderSchema(**order) for order in orders]

    async def get_products(self) -> list[ProductSchema]:
        products = await self._get_all_products()
        return [ProductSchema(**product) for product in products]