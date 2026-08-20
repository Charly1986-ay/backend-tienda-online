from contextlib import asynccontextmanager

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.articles.models import Article
from app.api.v1.articles.schemas import ArticleCreate, ArticleUpdate, UpdatePrice
from app.api.v1.articles.schemas import UpdateCategory, UpdateBrand, UpdateStatus

from app.api.v1.movements.models import GenericActivityLog
from app.api.v1.movements.enums import MovementType, TargetType

from app.core.pagination import get_pagination

from app.api.v1.articles.repository import ArticleRepository
from app.api.v1.brands.repository import BrandRepository
from app.api.v1.categories.repository import CategoryRepository
from app.api.v1.movements.repository import ActivityRepository
from app.core.exceptions import ArticleNotFound


class ArticleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.article_repo = ArticleRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)
        self.brand_repo = BrandRepository(db=db)
        self.category_repo = CategoryRepository(db=db)


    async def _get_brand_name(self, brand_id: int | None) -> str:
        '''Método auxiliar para obtener el nombre de la brand de forma segura.'''
        if not brand_id:
            return 'Generica y/o Desconocida'
        brand = await self.brand_repo.get(brand_id=brand_id)
        return brand.name if brand else 'Generica y/o Desconocida'

    async def _get_category_name(self, category_id: int | None) -> str:
        '''Método auxiliar para obtener el nombre de la categoría de forma segura.'''
        if not category_id:
            return 'Sin Categoría'
        category = await self.category_repo.get(category_id=category_id)
        return category.name if category else 'Sin Categoría'

    async def _get_or_404(self, article_id: int) -> Article:
        '''Método auxiliar para buscar el artículo o lanzar la excepción si no existe.'''
        article_db = await self.article_repo.get(article_id=article_id)
        if not article_db:
            raise ArticleNotFound()
        return article_db

    async def _update_article_data(self, article_db: Article, data: object) -> Article:
        '''Método auxiliar para aplicar los cambios permitidos del esquema.'''
        updates = data.model_dump(exclude_unset=True)
        return await self.article_repo.update(article=article_db, updates=updates)

    async def _log_activity(
        self, 
        user_id: int, 
        target_id: str, 
        movement_type: MovementType, 
        details: str
    ) -> None:
        '''Método auxiliar para registrar la actividad o movimiento.'''
        log_db = GenericActivityLog(
            user_id=user_id,
            target_type=TargetType.ARTICLE.value,
            target_id=target_id,
            movement_type=movement_type.value,
            details=details
        )
        await self.activity_repo.create_movement(log=log_db) 

    @asynccontextmanager
    async def _transaction(self):
        """Context manager para manejar transacciones, commit, rollback y refresh."""
        try:
            yield
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def create_article(self, article: ArticleCreate, user_id: int) -> Article:
        async with self._transaction():
            article_db = Article(
                detail=article.detail,
                stock=article.stock,                
                cost=article.cost,
                price=article.price,
                brand_id=article.brand_id,
                category_id=article.category_id,
                units_type=article.units_type,
                image_url=article.image_url
            )            
            next_article = await self.article_repo.create_article(article=article_db)

            brand_name = await self._get_brand_name(next_article.brand_id)
            category_name = await self._get_category_name(next_article.category_id)

            await self._log_activity(
                user_id=user_id,
                target_id=str(next_article.id),
                movement_type=MovementType.CREATED,
                details=f'Nuevo artículo NRO: {next_article.id} de la categoría {category_name} y brand {brand_name}'
            )
            await self.db.refresh(next_article)
            return next_article        

    async def update_article(self, data: ArticleUpdate, article_id: int, user_id: int) -> Article:
        async with self._transaction():
            article_db = await self._get_or_404(article_id)
            next_article = await self._update_article_data(article_db, data)

            await self._log_activity(
                user_id=user_id,
                target_id=str(next_article.id),
                movement_type=MovementType.UPDATED,
                details=f'Se actualizo el artículo NRO: {next_article.id}'
            )            
            await self.db.refresh(next_article)
            return next_article

    async def change_status(self, data: UpdateStatus, article_id: int, user_id: int) -> Article:
        async with self._transaction():
            article_db = await self._get_or_404(article_id)
            previous_state = article_db.status
            
            next_article = await self._update_article_data(article_db, data)

            await self._log_activity(
                user_id=user_id,
                target_id=str(next_article.id),
                movement_type=MovementType.ARTICLE_STATUS,
                details=f'Se modifico el estado del artículo NRO: {next_article.id} de {previous_state} a {next_article.status}'
            )
            await self.db.refresh(next_article)
            return next_article

    async def change_category(self, data: UpdateCategory, article_id: int, user_id: int) -> Article:
        async with self._transaction():    
            article_db = await self._get_or_404(article_id)
            previous_category = await self._get_category_name(article_db.category_id)
                                    
            next_article = await self._update_article_data(article_db, data)
            next_category = await self._get_category_name(next_article.category_id)
    
            await self._log_activity(
                user_id=user_id,
                target_id=str(next_article.id),
                movement_type=MovementType.CATEGORY_CHANGE,
                details=f'Se modifico la categoría del artículo NRO: {next_article.id} de {previous_category} a {next_category}'
            )    
            await self.db.refresh(next_article)
            return next_article

    async def change_brand(self, data: UpdateBrand, article_id: int, user_id: int) -> Article:
        async with self._transaction():        
            article_db = await self._get_or_404(article_id)
            previous_brand = await self._get_brand_name(article_db.brand_id)
                                                           
            next_article = await self._update_article_data(article_db, data)
            next_brand = await self._get_brand_name(next_article.brand_id)
        
            await self._log_activity(
                user_id=user_id,
                target_id=str(next_article.id),
                movement_type=MovementType.BRAND_CHANGE,
                details=f'Se modifico la brand del artículo NRO: {next_article.id} de {previous_brand} a {next_brand}'
            )        
            await self.db.refresh(next_article)
            return next_article

    async def change_price(self, data: UpdatePrice, article_id: int, user_id: int) -> Article:
        async with self._transaction():        
            article_db = await self._get_or_404(article_id)
            previous_cost = article_db.cost             
            previous_price = article_db.price
                                                   
            next_article = await self._update_article_data(article_db, data)        
                                   
            next_price = next_article.price
            next_cost = next_article.cost
            
            await self._log_activity(
                user_id=user_id,
                target_id=str(next_article.id),
                movement_type=MovementType.PRICE_UPDATE,
                details=f'Se modifico el precio del artículo NRO: {next_article.id}. Precio de {previous_price} a {next_price}, costo de {previous_cost} a {next_cost}'
            )            
            await self.db.refresh(next_article)
            return next_article


    async def get_all_pagination(
        self,        
        page_size: int = 10,  
        page: int = 1,
        detail: str | None = None,
        brand: str | None = None,     
        category: str | None = None,
        sort_by: str = 'id',            
        sort_order: str = 'asc'        
    ) -> dict:         
        counter = await self.article_repo.count_all(
            detail=detail, 
            brand=brand, 
            category=category
        )

        pagination = get_pagination(
            counter=counter,
            page=page,
            page_size=page_size
        )

        rows = await self.article_repo.get_all_pagination(
            page_size=pagination['page_size'],
            offset=pagination['offset'],
            detail=detail, 
            brand=brand,
            category=category,
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