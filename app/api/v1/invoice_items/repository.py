from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.v1.invoice_items.models import InvoiceItem

class InvoiceItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_items(self, invoice_id: int) -> List[InvoiceItem]:        
        result = await self.db.exec(
            select(InvoiceItem).where(InvoiceItem.invoice_id == invoice_id)
        )            
        return list(result.all())

    async def create_item(self, item: InvoiceItem) -> InvoiceItem:
        self.db.add(item)
        await self.db.flush()
        return item