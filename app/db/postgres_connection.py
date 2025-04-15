import asyncpg
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

async def connect_to_db():
    global db_pool
    try:
        db_pool = await asyncpg.create_pool(
            host=settings.database_host,
            port=settings.database_port,
            user=settings.database_user,
            password=settings.database_password,
            database=settings.database_name,
            min_size=1,
            max_size=10,
        )
        logger.info("Database pool created")
    except Exception as e:
        logger.error(f"Failed to create database pool: {e}")
        raise e
    
async def close_db_connection():
    await db_pool.close()
    logger.info("Database pool closed")

async def get_connection():
    async with db_pool.acquire() as conn:
        yield conn