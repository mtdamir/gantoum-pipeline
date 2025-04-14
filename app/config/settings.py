from pydantic_settings import BaseSettings
import json

class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_name: str
    database_host: str
    database_port: int
    jwt_secret_key: str
    jwt_algorithm: str
    airflow_secret_key: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()