"""
Configurações do sistema via variáveis de ambiente.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # APP
    APP_NAME: str = "ERP Material de Construção"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # DATABASE
    DATABASE_URL: str = "postgresql://erp_user:erp_pass_123@db:5432/erp_material"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "erp_material"
    DB_USER: str = "erp_user"
    DB_PASSWORD: str = "erp_pass_123"

    # SECURITY
    SECRET_KEY: str = "super-secret-key-erp-material-2026-mude-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # WHATSAPP
    WHATSAPP_API_URL: str = "http://evolution-api:8080"
    WHATSAPP_API_KEY: str = ""
    WHATSAPP_INSTANCE_NAME: str = "erp_material"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self) -> List[str]:
        return self.CORS_ORIGINS.split(",")


settings = Settings()