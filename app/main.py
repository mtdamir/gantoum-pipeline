from fastapi import FastAPI
from routes.users_router import router as users_router
from  routes.purchases_router import router as purchases_router
from db.postgres_connection import connect_to_db, close_db_connection
from db.create_user_table import create_users_table
from db.create_order_table import create_orders_table
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    await connect_to_db()
    await create_users_table() 
    await create_orders_table()
    logger.info("Application startup complete.")
    yield
    logger.info("Shutting down the application...")
    await close_db_connection()
    logger.info("Application shutdown complete.")

app = FastAPI(
    title="Gantoum Pipeline API",
    description="API for managing users and purchases in Gantoum pipeline.",
    version="1.0.0",
    lifespan=lifespan  
)

app.include_router(users_router, prefix="/users", tags=["users-auth"])
app.include_router(purchases_router, prefix="/purchases", tags=["purchases"])

