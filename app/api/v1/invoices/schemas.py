from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.api.v1.invoice_items.schemas import InvoiceItemCreate
from app.api.v1.invoice_items.schemas import InvoiceItemResponse
from app.api.v1.invoices.enums import InvoiceStatus


class InvoiceBase(BaseModel):
    client_id: int

    @computed_field
    @property
    def total(self) -> Decimal:
        total = Decimal("0.00")
        if getattr(self, "items", None):
            for item in self.items:
                total += item.subtotal
        return total


class InvoiceCreate(InvoiceBase):
    items: list[InvoiceItemCreate]


class UpdateInvoiceStatus(BaseModel):
    status: InvoiceStatus


class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    date: datetime
    status: InvoiceStatus
    fullname: Optional[str] = None
    items: list[InvoiceItemResponse] = Field(default_factory=list)
      
    model_config = ConfigDict(from_attributes=True)


class InvoicePaginationResponse(BaseModel):  
    counter: int
    pages: int
    offset: int
    page: int
    page_size: int
    invoices: list[InvoiceResponse]  

    model_config = ConfigDict(from_attributes=True)