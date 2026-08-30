from __future__ import annotations

from typing import TYPE_CHECKING

from contextlib import asynccontextmanager

from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.invoice_items import ItemsService
from app.enums.invoices import InvoiceStatus
from app.models.invoice import Invoice
from app.api.v1.public.checkout.schemas import InvoiceCreate

from app.repositories.invoices import InvoiceRepository

from app.models.movements import GenericActivityLog
from app.enums.movements import MovementType, TargetType
from app.repositories.movements import ActivityRepository

from app.services.payment import PaymentService

from app.core.exceptions import InvoiceNotFound
from app.core.pagination import get_pagination


if TYPE_CHECKING:    
    from app.api.v1.admin.invoices.schemas import UpdateInvoiceStatus    


class InvoiceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.invoice_repo = InvoiceRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)
        
        self.payment_service = PaymentService(db=db)
        self.items_service = ItemsService(db=db)


    @asynccontextmanager
    async def _transaction(self):
        """Context manager para manejar transacciones, commit, rollback y refresh."""
        try:
            yield
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def Checkout(
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

            # generamos el codigo de factura
            invoice_db.invoice_number = InvoiceCreate.generate_code(
                id=invoice_db.id
            )
                    
            # cargamos los items
            await self.items_service.insert_items(
                items=data.items,
                invoice=invoice_db,
                user_id=user_id
            )

            # hacemos el pago    
            await self.payment_service.create_payment(
                card=data.card,
                #user_id=user_id,
                invoice=invoice_db
            )

            # registramos actividad
            log = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.INVOICE.value,
                target_id=str(invoice_db.id),
                movement_type=MovementType.CREATED.value,
                details=(
                    f'Se creó la factura {invoice_db.invoice_number} '
                    f'x ${invoice_db.total} '
                    f'al cliente NRO {invoice_db.client_id}'
                )
            )
            await self.activity_repo.create_movement(log=log)

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
                details=(
                    f'Se modificó el estado de la factura' 
                    f'{invoice_db.invoice_number} de {status_prev}'
                    f'a {invoice.status}'
                )
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
            invoice_dict['fullname'] = user.full_name         
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