from typing import Any, Dict

from sqlalchemy.orm import selectinload
from sqlmodel import Sequence, asc, desc, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.users import User

from ..models.invoice import Invoice
from ..enums.invoices import InvoiceStatus


class InvoiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get(self, invoice_id: int) -> Invoice | None:
        query = (
            select(Invoice)
            .options(
                selectinload(Invoice.client),
                selectinload(Invoice.items)
            )
            .where(Invoice.id == invoice_id)
        )
        result = await self.db.exec(query)
        return result.first()


    async def get_number_invoice(self, number_invoice: str) -> Invoice | None:
        query = (
            select(Invoice)
            .options(selectinload(Invoice.client))
            .where(Invoice.invoice_number == number_invoice)
        )
        result = await self.db.exec(query)
        return result.first()


    async def count_all(
        self, 
        status: InvoiceStatus | None = None,
        client_id: int | None = None,
        full_name: str | None = None  
    ) -> int:            
        query = select(func.count()).select_from(Invoice)

        if full_name:
            query = query.join(Invoice.client)

        if status:
            query = query.where(Invoice.status == status)                
            
        if client_id:
            query = query.where(Invoice.client_id == client_id)

        if full_name:
            query = query.where(User.full_name.ilike(f'%{full_name}%'))
            
        result = await self.db.exec(query)
        return result.first() or 0


    async def get_all_pagination(
        self, 
        page_size: int, 
        offset: int, 
        status: InvoiceStatus | None = None,                
        client_id: int | None = None,
        full_name: str | None = None,  
        sort_by: str = 'id',
        sort_order: str = 'asc'
    ) -> Sequence[tuple[Invoice, User]]:
        
        query = select(Invoice, User).join(Invoice.client)

        if status:  
            query = query.where(Invoice.status == status)                                
            
        if client_id:
            query = query.where(Invoice.client_id == client_id)

        if full_name:
            query = query.where(User.full_name.ilike(f'%{full_name}%'))
            
        allowed_columns = {
            'id': Invoice.id,
            'number': Invoice.invoice_number,
            'fullname': User.full_name,
            'date': Invoice.date,        
            'total': Invoice.total,
        }
            
        column_to_sort = allowed_columns.get(sort_by, Invoice.id)
            
        if sort_order.lower() == 'desc':
            query = query.order_by(desc(column_to_sort))
        else:
            query = query.order_by(asc(column_to_sort))
                
        query = query.offset(offset).limit(page_size)
            
        result = await self.db.exec(query)
        return result.all()    


    async def create_invoice(self, invoice: Invoice) -> Invoice:
        """Solo añade la factura base para que la BD le asigne un ID."""
        self.db.add(invoice)
        await self.db.flush()
        return invoice


    async def update(self, invoice: Invoice, updates: Dict[str, Any]) -> Invoice:
        for key, value in updates.items():
            setattr(invoice, key, value)    
        self.db.add(invoice)
        return invoice    