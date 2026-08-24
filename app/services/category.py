from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.articles import Article
from app.repositories.article import ArticleRepository
from app.repositories.categories import CategoryRepository
from app.core.exceptions import CategoryNotFound


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_repo = CategoryRepository(db=db)
        self.article_repo = ArticleRepository(db=db)


    async def get_articles_by_category(self, category_id: int) -> list[Article]:
        category_db = await self.category_repo.get(
            category_id=category_id
        )
        if not category_db:
            raise CategoryNotFound()
        return await self.article_repo.get_by_category(
            category_id=category_id
        )