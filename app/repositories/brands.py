from typing import Dict

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.brands import Brand

class BrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, brand_id: int) -> Brand | None:
        return await self.db.get(Brand, brand_id)


    async def get_brand_by_name(self, name: str) -> Brand:
        result = await self.db.exec(select(Brand).where(
            Brand.name == name)
        )        
        return result.one_or_none()


    async def create(self, data: Brand) -> Brand:
            self.db.add(data)
            await self.db.flush()
            return data
    
    
    async def update(self, brand: Brand, updates: Dict[str, str]) -> Brand:
        for key, value in updates.items():
            setattr(brand, key, value)
            
        self.db.add(brand)
        return brand