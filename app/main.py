from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from app.core.config import settings
from app.core.db import init_db

from app.api.v1.articles.router import router as articles_router
from app.api.v1.auth.router import router as auth_router
from app.api.v1.invoices.router import router as invoice_router
from app.api.v1.users.router import router as user_router
from app.api.v1.categories.router import router as categories_router
from app.api.v1.brands.router import router as brands_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):    
    await init_db()
    yield

app = FastAPI(    
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True}
)

# --- 2. Añade esta función para limpiar el candado en Swagger ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# ----------------------------------------------------------------

os.makedirs("app/uploads", exist_ok=True)

# Monta la carpeta apuntando correctamente al directorio físico dentro de app
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Configura los orígenes permitidos
origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # React por defecto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles_router, prefix="/api/v1/articles", tags=["Articles"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(invoice_router, prefix="/api/v1/invoices", tags=["Invoices"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(brands_router, prefix="/api/v1/brands", tags=["Brands"])

@app.get('/')
def get_root():
    return {'message': 'Bienvenido a mi tienda'}