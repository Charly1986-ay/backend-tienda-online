from decimal import Decimal

import stripe

from app.core.config import settings
from app.enums.payments import TypeCurrency


class StripeService:

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.STRIPE_SECRET_KEY
        stripe.api_key = self.api_key

    async def create_payment_method(
        self,
        card: dict, # card={"token": "tok_visa"}
    ) -> stripe.PaymentMethod:

        if not card:
            raise ValueError(
                "Se requiere un método de pago."
            )

        try:
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card=card,
            )

            return payment_method

        except stripe.StripeError as e:
            print(e.user_message)

    def create_payment(
        self,
        #client_id: str,       
        amount: Decimal,
        currency: TypeCurrency,
        payment_method_id: str,
    ) -> stripe.PaymentIntent | None:

        amount_cents = int(amount * 100)

        try:
            payment = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                #customer=client_id,
                payment_method=payment_method_id,
                payment_method_types=["card"],
                confirm=True,                
            )

            return payment

        except stripe.CardError as e:
            print(e.user_message)
            return None

        except stripe.StripeError as e:
            print(e.user_message)
            return None


'''
payment_method_id = await stripe_service.create_payment_method(card)

payment = stripe_service.create_payment(
    client_id=...,
    article_id=...,
    amount=...,
    currency=...,
    payment_method_id=payment_method_id,
)
'''