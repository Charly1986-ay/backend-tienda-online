from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.articles.repository import ArticleRepository
from app.api.v1.articles.schemas import UpdateStock
from app.api.v1.invoice_items.schemas import InvoiceItemCreate
from app.api.v1.invoices.models import Invoice
from app.api.v1.movements.enums import MovementType, TargetType
from app.api.v1.movements.models import GenericActivityLog
from app.api.v1.movements.repository import ActivityRepository
from app.core.exceptions import ArticleNotFound, InsufficientInventory 
from app.core.exceptions import PriceMismatch

from .models import InvoiceItem
from .repository import InvoiceItemRepository

class InvoiceItemsService:    
    def __init__(self, db: AsyncSession):
        self.items_repo = InvoiceItemRepository(db=db)
        self.article_repo = ArticleRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)


    async def create_items(
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


    async def get_items(self, invoice_id: int) -> list[InvoiceItem]:
        items = await self.items_repo.get_items(invoice_id=invoice_id) or []
        return items