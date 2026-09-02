from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field

from app.api.v1.public.invoice_items.schemas import ItemCreate 
from app.api.v1.public.invoice_items.schemas import ItemPublic
from app.api.v1.public.payments.schemas import CardStripe
from app.enums.invoices import InvoiceStatus


class InvoiceBase(BaseModel):    
    items: list[ItemCreate]

    @computed_field
    @property
    def total(self) -> Decimal:
        total = Decimal("0.00")
        if getattr(self, "items", None):
            for item in self.items:
                total += item.subtotal
        return total


class InvoiceCreate(InvoiceBase):
    client_id: int
    card: CardStripe

    @staticmethod
    def generate_code(id: int) -> str:
        current_year = datetime.now().year
        formatted_id = str(id).zfill(4)
        return f"FAC-{current_year}-{formatted_id}"


class InvoicePublic(InvoiceBase):
    invoice_number: str
    date: datetime
    status: InvoiceStatus
    fullname: Optional[str] = None 
    items: list[ItemPublic]   
      
    model_config = ConfigDict(from_attributes=True)