import logging
from datetime import datetime
from db.postgres_connection import get_connection

logger = logging.getLogger(__name__)

async def create_users_table():
    async for conn in get_connection():
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS public.users (
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    refresh_token TEXT
                );
            """)
            logger.info("Users table created successfully.")
        except Exception as e:
            logger.error(f"Error creating users table: {e}")
            raise

async def create_user(name: str, email: str, password_hash: str, role: str = "user"):
    async for conn in get_connection():
        try:
            result = await conn.fetchrow("""
                INSERT INTO public.users (name, email, password_hash, role, created_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING user_id, name, email, role, created_at;
            """, name, email, password_hash, role, datetime.now())  
            return dict(result)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

async def get_user_by_id(user_id: int):
    async for conn in get_connection():
        try:
            result = await conn.fetchrow("""
                SELECT user_id, name, email, password_hash, role, created_at, updated_at, refresh_token
                FROM public.users
                WHERE user_id = $1;
            """, user_id)
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Error fetching user by id: {e}")
            raise

async def get_user_by_email(email: str):
    async for conn in get_connection():
        try:
            result = await conn.fetchrow("""
                SELECT user_id, name, email, password_hash, role, created_at, updated_at, refresh_token
                FROM public.users
                WHERE email = $1;
            """, email)
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            raise

async def update_user_refresh_token(email: str, refresh_token: str):
    async for conn in get_connection():
        try:
            await conn.execute("""
                UPDATE public.users
                SET refresh_token = $1, updated_at = $2
                WHERE email = $3;
            """, refresh_token, datetime.now(), email)  
        except Exception as e:
            logger.error(f"Error updating refresh token: {e}")
            raise