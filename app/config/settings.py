from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    AIRFLOW_SECRET_KEY:str

    gantoum_product_url:str

    model_config = SettingsConfigDict(env_file="./ .env", env_file_encoding="utf-8")

settings = Settings()