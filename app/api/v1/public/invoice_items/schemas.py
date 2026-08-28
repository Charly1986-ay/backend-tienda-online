from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, computed_field


class ItemBase(BaseModel):
    article_id: int
    units: int = Field(default=1, ge=1)    
    price: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return Decimal(str(self.units * self.price))

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    detail: str
        
    model_config = ConfigDict(from_attributes=True)