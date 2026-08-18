from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(default="HS256", env="JWT_ALG")
    JWT_EXPIRES_MIN: int = Field(default=60*24, env="JWT_EXPIRES_MIN")
    STRIPE_SECRET_KEY: str = Field(..., env="STRIPE_SECRET_KEY")
    PROJECT_NAME: str = "Tienda Online"    

    # --- NUEVAS VARIABLES PARA EL SISTEMA DE CORREOS ---
    MAIL_USERNAME: str = Field(default="", env="MAIL_USERNAME")
    MAIL_PASSWORD: str = Field(default="", env="MAIL_PASSWORD")
    MAIL_FROM: str = Field(..., env="MAIL_FROM") # Requerido
    MAIL_PORT: int = Field(default=1025, env="MAIL_PORT")
    MAIL_SERVER: str = Field(default="localhost", env="MAIL_SERVER")
    MAIL_FROM_NAME: str = Field(default="Tienda Online", env="MAIL_FROM_NAME")
    
    class Config:
        env_file = ".env"


try:
    settings = Settings()
except Exception as e:
    print(f"Error al cargar la configuración: {e}")
    raise e