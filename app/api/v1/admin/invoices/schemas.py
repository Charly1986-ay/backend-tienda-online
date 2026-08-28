from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


from app.enums.invoices import InvoiceStatus


class UpdateInvoiceStatus(BaseModel):
    status: InvoiceStatus


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    date: datetime
    status: InvoiceStatus
    fullname: Optional[str] = None
    total: Decimal
      
    model_config = ConfigDict(from_attributes=True)


class InvoicePaginationResponse(BaseModel):  
    counter: int
    pages: int
    offset: int
    page: int
    page_size: int
    invoices: list[InvoiceResponse]  

    model_config = ConfigDict(from_attributes=True)