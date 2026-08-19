from typing import Dict, List, Any

from sqlalchemy.orm import selectinload
from sqlmodel import Sequence, func, select, asc, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.articles.models import Article
from app.api.v1.brands.models import Brand
from app.api.v1.categories.models import Category

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

    async def get_by_category(self, category_id: int) -> list[Article]:
        """Usa selectinload en lugar de join si solo quieres los datos relacionados"""
        result = await self.db.exec(
            select(Article)
            .options(selectinload(Article.category))
            .options(selectinload(Article.brand))
            .where(Article.category_id == category_id)
        )           
        return result.all()

    async def get_by_brand(self, brand_id: int) -> list[Article]:        
        """Idem para la marca"""
        result = await self.db.exec(
            select(Article)
            .options(selectinload(Article.category))
            .options(selectinload(Article.brand))
            .where(Article.brand_id == brand_id)
        )           
        return result.all()


    async def count_all(
        self, 
        detail: str | None = None,
        brand: str | None = None, 
        category: str | None = None            
    ) -> int:        
        query = select(func.count()).select_from(Article)        
        
        query = query.join(Brand).join(Category)

        if detail:
            query = query.where(Article.detail.ilike(f'%{detail}%'))
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
        detail: str | None = None,
        brand: str | None = None, 
        category: str | None = None,        
        sort_by: str = 'id',
        sort_order: str = 'asc'
    ) -> Sequence[tuple[Article, Category, Brand]]:
        query = select(Article, Category, Brand).join(Brand).join(Category)

        if detail:  
            query = query.where(Article.detail.ilike(f'%{detail}%')) 
        if brand:
            query = query.where(Brand.name.ilike(f'%{brand}%'))
        if category:
            query = query.where(Category.name.ilike(f'%{category}%'))                   
        
        allowed_columns = {
            'id': Article.id,
            'name': Article.detail,        
            'brand': Brand.name,
            'category': Category.name
        }
        
        # Selecciona la columna o usa 'id' por defecto si mandan un campo inválido
        column_to_sort = allowed_columns.get(sort_by, Article.id)
        
        # Aplicar ordenamiento ASC o DESC
        if sort_order.lower() == 'desc':
            query = query.order_by(desc(column_to_sort))
        else:
            query = query.order_by(asc(column_to_sort))
            
        # Aplicar paginación al final
        query = query.offset(offset).limit(page_size)
        
        result = await self.db.exec(query)
        return result.all()


    async def create_article(self, article: Article) -> Article:
        self.db.add(article)
        await self.db.flush()
        return article


    async def update(self, article: Article, updates: Dict[str, Any]) -> Article:
        for key, value in updates.items():
            setattr(article, key, value)

        self.db.add(article)
        return article