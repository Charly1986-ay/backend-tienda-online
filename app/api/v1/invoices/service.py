from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.articles.repository import ArticleRepository
from app.api.v1.articles.schemas import UpdateStock
from app.api.v1.invoices.enums import InvoiceStatus
from app.api.v1.invoices.models import Invoice
from app.api.v1.invoices.schemas import InvoiceCreate, UpdateInvoiceStatus
from app.api.v1.invoices.repository import InvoiceRepository

from app.api.v1.invoice_items.models import InvoiceItem
from app.api.v1.invoice_items.repository import InvoiceItemRepository

from app.api.v1.movements.models import GenericActivityLog
from app.api.v1.movements.enums import MovementType, TargetType
from app.api.v1.movements.repository import ActivityRepository

from app.core.exceptions import ArticleNotFound, InsufficientInventory
from app.core.exceptions import InvoiceNotFound, PriceMismatch
from app.core.pagination import get_pagination


class InvoiceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.invoice_repo = InvoiceRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)
        self.item_repo = InvoiceItemRepository(db=db)
        self.article_repo = ArticleRepository(db=db)

    def _generate_invoice_number(self, sale_id: int) -> str:        
        """Tu función para generar el código alfanumérico."""
        current_year = datetime.now().year
        formatted_id = str(sale_id).zfill(4)
        return f'FAC-{current_year}-{formatted_id}'

    @asynccontextmanager
    async def _transaction(self):
        """Context manager para manejar transacciones, commit, rollback y refresh."""
        try:
            yield
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def create_invoice(
        self, 
        data: InvoiceCreate, 
        user_id: int
    ) -> Invoice:
        async with self._transaction():
            invoice_db = Invoice(
                total=data.total, 
                client_id=data.client_id
            )
            await self.invoice_repo.create_invoice(invoice_db)
        
            invoice_db.invoice_number = self._generate_invoice_number(
                invoice_db.id
            )
                    
            for item in data.items:
                article_db = await self.article_repo.get(
                    article_id=item.article_id
                )

                if not article_db:
                    raise ArticleNotFound()

                prev_stock = article_db.stock

                if article_db.stock < item.units:
                    raise InsufficientInventory()

                if article_db.price < item.price:
                    raise PriceMismatch()

                item_db = InvoiceItem(
                    invoice_id=invoice_db.id,
                    article_id=item.article_id,
                    detail=article_db.detail,
                    units=item.units,
                    price=item.price,
                    subtotal=item.subtotal  
                )
                await self.item_repo.create_item(item_db)   

                data_article = UpdateStock(
                    units=(prev_stock - item.units)
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
            
            log_invoice = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.INVOICE.value,
                target_id=str(invoice_db.id),
                movement_type=MovementType.CREATED.value,
                details=f'Se creó la factura {invoice_db.invoice_number} x ${invoice_db.total} al cliente NRO {invoice_db.client_id}'
            )
            await self.activity_repo.create_movement(log=log_invoice)

            await self.db.refresh(invoice_db)            
            return invoice_db


    async def change_status(
        self, 
        data: UpdateInvoiceStatus, 
        invoice_id: int,
        user_id: int
    ) -> Invoice:  
        async with self._transaction():
            invoice_db = await self.invoice_repo.get(invoice_id=invoice_id)            

            if not invoice_db:
                raise InvoiceNotFound()

            status_prev = invoice_db.status
            
            updates = data.model_dump(exclude_unset=True)
        
            invoice = await self.invoice_repo.update(
                invoice=invoice_db,
                updates=updates
            )

            log = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.INVOICE.value,
                target_id=str(invoice_db.id),
                movement_type=MovementType.INVOICE_STATUS.value,
                details=f'Se modificó el estado de la factura {invoice_db.invoice_number} de {status_prev} a {invoice.status}'
            )
            await self.activity_repo.create_movement(log=log)
        
            await self.db.refresh(invoice)

            return invoice


    async def get_all_pagination(
        self,         
        page_size: int,    
        page: int,    
        status: InvoiceStatus | None = None,                
        client_id: int | None = None,
        full_name: str | None = None,                 
        sort_by: str = 'id',
        sort_order: str = 'asc'
    ) -> dict:
        counter = await self.invoice_repo.count_all(
            status=status,
            client_id=client_id,
            full_name=full_name
        )

        pagination = get_pagination(
            counter=counter,
            page=page,
            page_size=page_size
        )

        rows = await self.invoice_repo.get_all_pagination(
            page_size=pagination['page_size'],
            offset=pagination['offset'],
            status=status,
            client_id=client_id,
            full_name=full_name,
            sort_by=sort_by,           
            sort_order=sort_order      
        )

        invoice_list = []
        for invoice, user in rows:
            invoice_dict = invoice.model_dump()
            invoice_dict['full_name'] = user.full_name         
            invoice_list.append(invoice_dict)

        return {
            'counter': counter,
            'pages': pagination['pages'],
            'offset': pagination['offset'],
            'page': pagination['page'],
            'page_size': pagination['page_size'],
            'invoices': invoice_list
        }


    async def get_invoice(
        self,
        invoice_id: int
    ) -> Invoice:
        invoice_db = await self.invoice_repo.get(invoice_id=invoice_id)

        if not invoice_db:
            raise InvoiceNotFound()
        return invoice_db


    async def get_items(
        self,
        invoice_id: int
    ) -> List[InvoiceItem]:
        items = await self.item_repo.get_items(invoice_id=invoice_id) or []
        return items