import psycopg2
from psycopg2 import OperationalError
from app.config.settings import settings


def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_host,
            port=settings.postgres_port
        )
        return conn

    except OperationalError as e:
        print(f"Error connecting to our database: {e}")
        return None
    

def get_cursor(conn):
    conn = get_connection()
    if conn:
        return conn , conn.cursor()
    return None, None