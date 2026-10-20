from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.invoice import Invoice

from app.api.v1.admin.movements.enums import MovementType
from app.api.v1.admin.movements.enums import TargetType

from app.api.v1.shop.checkout.schemas import InvoiceCreate

from .repository import InvoiceRepository

from app.api.v1.shop.items.services import ItemsService
from app.api.v1.shop.payments.services import PaymentService
from app.api.v1.admin.movements.services import ActivityLogService

from app.core.exceptions import CartException    


class CheckOutService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.invoice_repo = InvoiceRepository(db=db)        
        
        self.payment_service = PaymentService(db=db)
        self.items_service = ItemsService(db=db)
        self.activity_log = ActivityLogService(db=db)


    async def checkout(
        self, 
        data: InvoiceCreate,        
        user_id: int
    )-> Invoice:
        if not data.items:
            raise CartException();

        try:
            invoice_db = Invoice(
                total=data.total,
                client_id=data.client_id
            )

            await self.invoice_repo.create_invoice(invoice_db)

            # Generamos el código de factura
            invoice_db.invoice_number = InvoiceCreate.generate_code(
                id=invoice_db.id
            )            

            # Cargamos los items
            await self.items_service.insert_items(
                items=data.items,
                invoice=invoice_db,
                user_id=user_id
            )

            # Hacemos el pago
            await self.payment_service.create_payment(
                card=data.card,
                invoice=invoice_db
            )

            # Registramos actividad
            await self.activity_log.create(
                user_id=user_id,
                target_id=str(invoice_db.id),
                target_type=TargetType.INVOICE,
                movement_type=MovementType.CREATED,
                details=(
                    f"Se creó la factura {invoice_db.invoice_number} "
                    f"x ${invoice_db.total} "
                    f"al cliente NRO {invoice_db.client_id}"
                ),
            )
            
            await self.db.refresh(invoice_db)
            return invoice_db
        except Exception as e:
            await self.db.rollback()
            raise e