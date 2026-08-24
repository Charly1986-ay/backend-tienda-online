from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.article import ArticleRepository
from app.api.v1.admin.articles.schemas import UpdateStock

from app.enums.movements import MovementType, TargetType

from app.repositories.movements import ActivityRepository
from app.core.exceptions import ArticleNotFound, InsufficientInventory 
from app.core.exceptions import PriceMismatch

from app.repositories.invoice_items import InvoiceItemRepository

if TYPE_CHECKING:
    from app.models.invoice import Invoice
    from app.models.invoice_items import InvoiceItem
    from app.models.movements import GenericActivityLog    
    from app.api.v1.public.invoice_items.schemas import InvoiceItemCreate

class InvoiceItemsService:    
    def __init__(self, db: AsyncSession):
        self.items_repo = InvoiceItemRepository(db=db)
        self.article_repo = ArticleRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)


    async def insert_items(
        self, 
        items: list[InvoiceItemCreate], 
        invoice: Invoice, 
        user_id: int
    ) -> None:
        for item in items:
            article_db = await self.article_repo.get(
                article_id=item.article_id
            )
        
            if not article_db:
                raise ArticleNotFound()
        
            prev_stock = article_db.stock
        
            if article_db.stock < item.units:
                raise InsufficientInventory()
        
            if article_db.price > item.price:
                raise PriceMismatch()
        
            item_db = InvoiceItem(
                invoice_id=invoice.id,
                article_id=item.article_id,
                detail=article_db.detail,
                units=item.units,
                price=item.price,
                subtotal=item.subtotal  
            )
            await self.items_repo.create_item(item_db)   
        
            data_article = UpdateStock(
                stock=(prev_stock - item.units)
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
                details=f'Se actualizó el stock artículo NRO. {item.article_id} de {prev_stock} a {new_article.stock} unidades'
            )
            await self.activity_repo.create_movement(log=log_stock)


    async def refund_items(
            self, 
            items: list[InvoiceItemCreate],            
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