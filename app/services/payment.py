from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.invoice import Invoice
from app.enums.payments import PaymentStatus, TypeCurrency
from app.models.payments import Payment
from app.repositories.payments import PaymentRepository
from app.services.stripe import StripeService
from app.core.exceptions import PaymentException


if TYPE_CHECKING:
    from app.api.v1.public.payments.schemas import CardStripe


class PaymentService:
    def __init__(self, db: AsyncSession):        
        self.payment_repo = PaymentRepository(db=db)
        self.stripe_service = StripeService()


    async def create_payment(
        self, 
        card: CardStripe, 
        #user_id: int, 
        invoice: Invoice
    ) -> None:
        data_dict = card.model_dump()  

        payment_method_id = await self.stripe_service.create_payment_method(
            card=data_dict
        )  

        payment_stripe = self.stripe_service.create_payment(
            # client_id=user_id,               
            amount=invoice.total,
            currency=TypeCurrency.USD.value,
            payment_method_id=payment_method_id,
        )
        
        # manejo de exceptions
        if payment_stripe is None or payment_stripe.id is None:
            raise PaymentException()
        
        payment = Payment(
            invoice_id=invoice.id,
            amount=invoice.total,               
            stripe_payment_intent_id=payment_stripe.id,
            status=PaymentStatus.COMPLETED.value
        )
        
        await self.payment_repo.create_payment(data=payment)