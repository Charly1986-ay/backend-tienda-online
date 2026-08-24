from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.enums.invoices import InvoiceStatus


class InvoiceBase(BaseModel):
    client_id: int


class InvoiceCreate(InvoiceBase):
    @staticmethod
    def generate_code(id: int) -> str:
        current_year = datetime.now().year
        formatted_id = str(id).zfill(4)
        return f"FAC-{current_year}-{formatted_id}"


class InvoicePublic(InvoiceBase):
    id: int
    invoice_number: str
    date: datetime
    status: InvoiceStatus
    fullname: Optional[str] = None
    total: Decimal 
      
    model_config = ConfigDict(from_attributes=True)