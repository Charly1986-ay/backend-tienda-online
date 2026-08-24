from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.brands import Brand

class BrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, brand_id: int) -> Brand | None:
        return await self.db.get(Brand, brand_id)