from typing import Dict

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.categories import Category

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get(self, category_id: int) -> Category | None:
        return await self.db.get(Category, category_id)


    async def get_category_by_name(self, name: str) -> Category:
        result = await self.db.exec(select(Category).where(
            Category.name == name)
        )        
        return result.one_or_none()


    async def get_category_by_slug(self, slug: str) -> Category:
        result = await self.db.exec(select(Category).where(
            Category.slug == slug)
        )        
        return result.one_or_none()


    async def create(self, data: Category) -> Category:
        self.db.add(data)
        await self.db.flush()
        return data


    async def update(self, category: Category, updates: Dict[str, str]) -> Category:
        for key, value in updates.items():
            setattr(category, key, value)
        
        self.db.add(category)
        return category