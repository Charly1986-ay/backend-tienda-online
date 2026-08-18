from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, computed_field


class InvoiceItemBase(BaseModel):
    article_id: int
    units: int = Field(default=1, ge=1)    
    price: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return Decimal(str(self.units * self.price))

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemResponse(InvoiceItemBase):
    id: int
    invoice_id: int
        
    model_config = ConfigDict(from_attributes=True)