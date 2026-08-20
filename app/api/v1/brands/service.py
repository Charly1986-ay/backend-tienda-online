from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.articles.models import Article
from app.api.v1.articles.repository import ArticleRepository
from app.api.v1.brands.repository import BrandRepository
from app.core.exceptions import BrandNotFound


class BrandService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.brand_repo = BrandRepository(db=db)
        self.article_repo = ArticleRepository(db=db)

    async def get_articles_by_brand(self, brand_id: int) -> list[Article]:
        brand_db = await self.brand_repo.get(brand_id=brand_id)
        if not brand_db:
            raise BrandNotFound()
        return await self.article_repo.get_by_brand(
            brand_id=brand_id
        )