import logging
from datetime import datetime
from db.postgres_connection import get_connection

logger = logging.getLogger(__name__)

async def create_orders_table():
    async for conn in get_connection():
        try:
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS public.orders (
                    order_id SERIAL PRIMARY KEY,
                    order_name VARCHAR(255) NOT NULL,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL CHECK (quantity > 0),
                    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE
                );
            """)
            logger.info("Orders table created successfully.")
        except Exception as e:
            logger.error(f"Error creating orders table: {e}")
            raise

async def create_order(user_id: int, product_id: int, quantity: int, order_name: str):
    async for conn in get_connection():
        try:
            result = await conn.fetchrow("""
                INSERT INTO public.orders (order_name, user_id, product_id, quantity, ordered_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING order_id, order_name, user_id, product_id, quantity, ordered_at;
            """, order_name, user_id, product_id, quantity, datetime.now())
            return dict(result)
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise

async def get_orders_by_user(user_id: int):
    async for conn in get_connection():
        try:
            result = await conn.fetch("""
                SELECT o.order_id, o.order_name, o.user_id, o.product_id, o.quantity, o.ordered_at, p.name as product_name
                FROM public.orders o
                JOIN public.products p ON o.product_id = p.id
                WHERE o.user_id = $1;
            """, user_id)
            return [dict(row) for row in result]
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            raise