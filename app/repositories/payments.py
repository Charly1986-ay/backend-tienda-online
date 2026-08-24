from typing import Dict, Any

from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.payments import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, data: Payment) -> Payment:
        """Solo añade el pago para que la BD le asigne un ID."""
        self.db.add(data)
        await self.db.flush()
        #return payment

    async def update(self, data: Payment, updates: Dict[str, Any]) -> Payment:
        for key, value in updates.items():
            setattr(data, key, value)    
        self.db.add(data)
        return data