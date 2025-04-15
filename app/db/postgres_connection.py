import asyncpg
import logging
from contextlib import asynccontextmanager
from config.settings import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_postgres_connection():
    pool = None
    try:
        pool = await asyncpg.create_pool(
            host=settings.database_host,
            port=settings.database_port,
            user=settings.database_user,
            password=settings.database_password,
            database=settings.database_name,
            min_size=1,
            max_size=10,
        )
        logger.info("Connected to PostgreSQL database.")
        yield pool
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL database pool: {e}")
        raise e
    finally:
        if pool:
            await pool.close()
            logger.info("PostgreSQL database pool closed.")