from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

# IMPORTA TUS MODELOS AQUÍ para que SQLModel los registre en el metadata
from app.models.articles import Article
from app.models.brands import Brand
from app.models.categories import Category
from app.models.invoice import Invoice
from app.models.items import InvoiceItem
from app.models.payments import Payment
from app.models.movements import GenericActivityLog

# 1. Creamos el motor asíncrono (create_async_engine)
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def init_db() -> None:    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session