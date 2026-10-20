from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.articles.repository import ArticleRepository
from app.api.v1.admin.articles.schemas import UpdateStock
from app.models.items import InvoiceItem

from app.models.movements import GenericActivityLog

from app.api.v1.admin.movements.enums import MovementType, TargetType

from app.api.v1.admin.movements.repositoy import ActivityRepository
from app.core.exceptions import ArticleNotFound

from .repository import ItemRepository

if TYPE_CHECKING:            
    from app.api.v1.shop.items.schemas import ItemCreate

class ItemsService:    
    def __init__(self, db: AsyncSession):
        self.items_repo = ItemRepository(db=db)
        self.article_repo = ArticleRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)


    async def refund_items(
        self, 
        items: list[ItemCreate],            
        user_id: int
    ) -> None:
        for item in items:
            article_db = await self.article_repo.get(
                article_id=item.article_id
            )
            
            if not article_db:
                raise ArticleNotFound()
            
            prev_stock = article_db.stock            
                   
            
            data_article = UpdateStock(
                stock=(prev_stock + item.units)
            )  
                            
            update_article = data_article.model_dump(
                exclude_unset=True
            )   
            
            new_article = await self.article_repo.update(
                article=article_db,
                updates=update_article
            )   
            
            log_stock = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.ARTICLE.value,
                target_id=str(item.article_id),
                movement_type=MovementType.STOCK_CHANGE.value,
                details=f'Devolucción de stock artículo NRO. {item.article_id} de {prev_stock} a {new_article.stock} unidades'
            )
            await self.activity_repo.create_movement(log=log_stock)


    async def get_items(self, invoice_id: int) -> list[InvoiceItem]:
        items = await self.items_repo.get_items(invoice_id=invoice_id) or []
        return items