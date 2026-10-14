from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.invoice import Invoice

from app.api.v1.admin.movements.enums import MovementType
from app.api.v1.admin.movements.enums import TargetType


from .repository import InvoiceRepository

from app.api.v1.admin.movements.services import ActivityLogService

from app.core.exceptions import InvoiceNotFound


if TYPE_CHECKING:    
    from app.api.v1.admin.invoices.schemas import UpdateInvoiceStatus    


class InvoiceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.invoice_repo = InvoiceRepository(db=db)       
        
        self.activity_log = ActivityLogService(db=db)


    async def change_status(
        self,
        data: UpdateInvoiceStatus,
        invoice_id: int,
        user_id: int
    ) -> Invoice:
        try:
            invoice_db = await self.invoice_repo.get(
                invoice_id=invoice_id
            )

            if not invoice_db:
                raise InvoiceNotFound()

            status_prev = invoice_db.status

            updates = data.model_dump(exclude_unset=True)

            invoice = await self.invoice_repo.update(
                invoice=invoice_db,
                updates=updates
            )

            await self.activity_log.create(
                user_id=user_id,
                target_id=str(invoice.id),
                target_type=TargetType.INVOICE,
                movement_type=MovementType.INVOICE_STATUS,
                details=(
                    f"Se modificó el estado de la factura "
                    f"{invoice.invoice_number} de {status_prev} "
                    f"a {invoice.status}"
                ),
            )

            await self.db.refresh(invoice)
            return invoice
        except Exception as e:
            await self.db.rollback()
            raise e