from __future__ import annotations

from typing import TYPE_CHECKING


from contextlib import asynccontextmanager

from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.articles.schemas import ArticleCreate
from app.api.v1.admin.articles.schemas import ArticleUpdate
from app.api.v1.admin.articles.schemas import UpdatePrice
from app.api.v1.admin.articles.schemas import UpdateCategory
from app.api.v1.admin.articles.schemas import UpdateBrand
from app.api.v1.admin.articles.schemas import UpdateStatus

from app.api.v1.admin.movements.enums import MovementType
from app.api.v1.admin.movements.enums import TargetType

from .repository import ArticleRepository
from app.api.v1.admin.brands.repository import BrandRepository
from app.api.v1.admin.categories.repository import CategoryRepository

from app.api.v1.admin.movements.services import ActivityLogService

from app.core.exceptions import ArticleExist, ArticleNotFound

if TYPE_CHECKING:
    from app.models.articles import Article

class ArticleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.article_repo = ArticleRepository(db=db)        
        self.brand_repo = BrandRepository(db=db)
        self.category_repo = CategoryRepository(db=db)
        self.activity_log = ActivityLogService(db=db)


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

    async def _exist_title(self, title: str) -> None:
        """Verifica si el título ya existe y lanza una excepción si es así."""
        exists = await self.article_repo.title_exists(title=title)
        if exists:
            raise ArticleExist()

    async def _get_or_404(self, article_id: int) -> Article:
        '''Método auxiliar para buscar el artículo o lanzar la excepción si no existe.'''
        article_db = await self.article_repo.get(article_id=article_id)
        if not article_db:
            raise ArticleNotFound()
        return article_db


    async def _update_article_data(
        self,
        article_db: Article,
        data: BaseModel
    ) -> Article:
        """Aplica los cambios permitidos al artículo."""
        updates = data.model_dump(exclude_unset=True)

        return await self.article_repo.update(
            article=article_db,
            updates=updates
        )

     
    @asynccontextmanager
    async def _transaction(self):
        """Context manager para manejar transacciones, commit, rollback y refresh."""
        try:
            yield
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def create_article(
        self, article: ArticleCreate, user_id: int
    ) -> Article:
        # 1. Validamos primero (si existe, lanzará la excepción automáticamente)
        await self._exist_title(title=article.title)

        # 2. Si pasa la validación, abrimos la transacción y creamos
        async with self._transaction():
            article_db = Article(
                title=article.title,
                slug=article.slug,
                detail=article.detail,
                stock=article.stock,
                cost=article.cost,
                price=article.price,
                brand_id=article.brand_id,
                category_id=article.category_id,
                units_type=article.units_type,
                image=article.image,
            )
            next_article = await self.article_repo.create_article(article=article_db)

            brand_name = await self._get_brand_name(next_article.brand_id)
            category_name = await self._get_category_name(next_article.category_id)

            await self.activity_log.create(
                user_id=user_id,
                target_id=str(next_article.id),
                target_type=TargetType.ARTICLE,
                movement_type=MovementType.CREATED,
                details=(
                    f"Nuevo artículo NRO: {next_article.id} "
                    f"de la categoría {category_name} "
                    f"y brand {brand_name}"
                ),
            )           
            await self.db.refresh(next_article)
            return next_article        

    async def update_article(
        self, data: ArticleUpdate, article_id: int, user_id: int
    ) -> Article:
        # 1. Obtenemos el artículo primero para conocer sus datos actuales
        article_db = await self._get_or_404(article_id)

        # 2. Solo validamos si envió un título nuevo y es diferente al que ya tenía
        if data.title is not None and data.title != article_db.title:
            await self._exist_title(title=data.title)

        async with self._transaction():
            next_article = await self._update_article_data(article_db, data)

            await self.activity_log.create(
                user_id=user_id,
                target_id=str(next_article.id),
                target_type=TargetType.ARTICLE,
                movement_type=MovementType.UPDATED,
                details=f"Se actualizó el artículo NRO: {next_article.id}",
            )
            await self.db.refresh(next_article)
            return next_article

    async def change_status(self, data: UpdateStatus, article_id: int, user_id: int) -> Article:
        async with self._transaction():
            article_db = await self._get_or_404(article_id)
            previous_state = article_db.status
            
            next_article = await self._update_article_data(article_db, data)

            await self.activity_log.create(
                user_id=user_id,
                target_id=str(next_article.id),
                target_type=TargetType.ARTICLE,
                movement_type=MovementType.ARTICLE_STATUS,
                details=(
                    f"Se modificó el estado del artículo NRO: {next_article.id} "
                    f"de {previous_state} a {next_article.status}"
                ),
            )
            await self.db.refresh(next_article)
            return next_article

    async def change_category(self, data: UpdateCategory, article_id: int, user_id: int) -> Article:
        async with self._transaction():    
            article_db = await self._get_or_404(article_id)
            previous_category = await self._get_category_name(article_db.category_id)
                                    
            next_article = await self._update_article_data(article_db, data)
            next_category = await self._get_category_name(next_article.category_id)
    
            await self.activity_log.create(
                user_id=user_id,
                target_id=str(next_article.id),
                target_type=TargetType.ARTICLE,
                movement_type=MovementType.CATEGORY_CHANGE,
                details=(
                    f"Se modificó la categoría del artículo NRO: {next_article.id} "
                    f"de {previous_category} a {next_category}"
                ),
            )   
            await self.db.refresh(next_article)
            return next_article

    async def change_brand(self, data: UpdateBrand, article_id: int, user_id: int) -> Article:
        async with self._transaction():        
            article_db = await self._get_or_404(article_id)
            previous_brand = await self._get_brand_name(article_db.brand_id)
                                                           
            next_article = await self._update_article_data(article_db, data)
            next_brand = await self._get_brand_name(next_article.brand_id)
        
            await self.activity_log.create(
                user_id=user_id,
                target_id=str(next_article.id),
                target_type=TargetType.ARTICLE,
                movement_type=MovementType.BRAND_CHANGE,
                details=(
                    f"Se modificó la brand del artículo NRO: {next_article.id} "
                    f"de {previous_brand} a {next_brand}"
                ),
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
            
            await self.activity_log.create(
                user_id=user_id,
                target_id=str(next_article.id),
                target_type=TargetType.ARTICLE,
                movement_type=MovementType.PRICE_UPDATE,
                details=(
                    f"Se modificó el precio del artículo NRO: {next_article.id}. "
                    f"Precio de {previous_price} a {next_price}, "
                    f"costo de {previous_cost} a {next_cost}"
                ),
            )            
            await self.db.refresh(next_article)
            return next_article    