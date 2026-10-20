from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.items import InvoiceItem

class ItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_item(self, item: InvoiceItem) -> InvoiceItem:
        self.db.add(item)
        await self.db.flush()
        return item