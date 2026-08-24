from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.payments import TypeCurrency


class PaymentCreate(BaseModel):    
    invoice_id: int
    amount: int   
    currency: str = TypeCurrency.USD         


class PaymentResponse(BaseModel):
    id: int   
    invoice_id: int
    amount: int
    currency: str
    status: str
    created_at: datetime    
    model_config = ConfigDict(from_attributes=True)


class CardStripe(BaseModel):
    token: str