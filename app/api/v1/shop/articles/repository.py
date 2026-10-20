from typing import Any, Dict

from sqlalchemy.orm import selectinload
from sqlmodel import Sequence, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.articles.enums import StatusArticle
from app.models.brands import Brand
from app.models.categories import Category

from app.models.articles import Article



class ArticleRepository:
    def __init__(self, db: AsyncSession):
      self.db = db


    async def get(self, article_id: int) -> Article | None:
      """Perfecto: Carga el artículo con sus relaciones de forma limpia"""
      query = (
          select(Article)
              .options(selectinload(Article.category))
              .options(selectinload(Article.brand))
              .where(Article.id == article_id)
      )
      result = await self.db.exec(query)
      return result.first()

    async def get_by_slug(self, slug: str) -> Article | None:
        query = (
            select(Article)
            .options(selectinload(Article.category))
            .options(selectinload(Article.brand))
            .where(Article.slug == slug)
        )
        result = await self.db.exec(query)
        return result.first()


    async def count_all(
        self, 
        title: str | None = None,
        brand: str | None = None, 
        category: str | None = None              
    ) -> int:     
        from app.models.articles import Article

        query = (
            select(func.count())
            .select_from(Article)
            .join(Brand)
            .join(Category)
            .where(Article.status == StatusArticle.AVAILABLE.value)
        )
    
        if title:
            query = query.where(Article.title.ilike(f'%{title}%'))
        if brand:
            query = query.where(Brand.name.ilike(f'%{brand}%'))
        if category:
            query = query.where(Category.name.ilike(f'%{category}%'))   
                
                
        result = await self.db.exec(query)
        return result.first() or 0


    async def get_all_pagination(
        self,
        page_size: int,
        offset: int,
        title: str | None = None,
        brand: str | None = None,
        category: str | None = None,
    ) -> Sequence[tuple[Article, Category, Brand]]:
        from app.models.articles import Article
        
        query = (
            select(Article, Category, Brand)
            .join(Brand)
            .join(Category)
            .where(Article.status == StatusArticle.AVAILABLE.value)
        )

        if title:
            query = query.where(Article.title.ilike(f"%{title}%"))
        if brand:
            query = query.where(Brand.name.ilike(f"%{brand}%"))
        if category:
            query = query.where(Category.name.ilike(f"%{category}%"))

        # Aplicar paginación al final
        query = query.offset(offset).limit(page_size)

        result = await self.db.exec(query)
        return result.all()


    async def update(self, article: Article, updates: Dict[str, Any]) -> Article:
        for key, value in updates.items():
            setattr(article, key, value)    
        self.db.add(article)
        return article