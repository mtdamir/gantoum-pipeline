from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str

    jwt_secret_key: str
    jwt_algorithm: str
    airflow_secret_key:str

    gantoum_product_url:str

    class Config:
        env_file = ".env"

settings = Settings()