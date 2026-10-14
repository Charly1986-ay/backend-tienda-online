from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel.ext.asyncio.session import AsyncSession

from .repository import ArticleRepository

from app.core.exceptions import ArticleNotFound

from app.core.pagination import get_pagination

if TYPE_CHECKING:
    from app.models.articles import Article


class ArticleQueryService:
    def __init__(self, db: AsyncSession):
        self.article_repo = ArticleRepository(db=db)


    async def _get_or_404(self, article_id: int) -> Article:
        '''Método auxiliar para buscar el artículo o lanzar la excepción si no existe.'''
        article_db = await self.article_repo.get(
            article_id=article_id
        )
        if not article_db:
            raise ArticleNotFound()
        return article_db


    async def get_all_pagination(
        self,        
        page_size: int = 10,  
        page: int = 1,
        title: str | None = None,
        brand: str | None = None,     
        category: str | None = None,
        status: str | None = None,
        sort_by: str = 'id',            
        sort_order: str = 'asc'        
    ) -> dict:         
        counter = await self.article_repo.count_all(
            title=title, 
            brand=brand, 
            category=category,
            status=status
        )
    
        pagination = get_pagination(
            counter=counter,
            page=page,
            page_size=page_size
        )
    
        rows = await self.article_repo.get_all_pagination(
            page_size=pagination['page_size'],
            offset=pagination['offset'],
            title=title, 
            brand=brand,
            category=category,
            status=status,
            sort_by=sort_by,           
            sort_order=sort_order      
        )
    
        articles_list = []
        for article, category_obj, brand_obj in rows:
            article_dict = article.model_dump()
            article_dict['category_name'] = category_obj.name
            article_dict['brand_name'] = brand_obj.name
            articles_list.append(article_dict)
    
        return {
            'counter': counter,
            'pages': pagination['pages'],
            'offset': pagination['offset'],
            'page': pagination['page'],
            'page_size': pagination['page_size'],
            'articles': articles_list
        }
    
    
    async def get_article_by_id(self, article_id: int) -> Article:
        return await self._get_or_404(article_id=article_id)    
    
    
    async def get_article_by_slug(self, slug: str) -> Article:
        article = await self.article_repo.get_by_slug(slug=slug)
    
        if article is None:
            raise ArticleNotFound()
        return article