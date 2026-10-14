from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.invoice import Invoice


class InvoiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_invoice(self, invoice: Invoice) -> Invoice:
        """Solo añade la factura base para que la BD le asigne un ID."""
        self.db.add(invoice)
        await self.db.flush()
        return invoice