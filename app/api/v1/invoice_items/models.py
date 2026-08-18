from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.api.v1.articles.models import Article
    from app.api.v1.invoices.models import Invoice


class InvoiceItem(SQLModel, table=True):
    __tablename__ = 'invoice_item'
    __table_args__ = {'extend_existing': True}    
    
    id: Optional[int] = Field(default=None, primary_key=True)  
    invoice_id: int = Field(foreign_key='invoice.id', index=True)  
    article_id: int = Field(foreign_key='article.id', index=True)  
    units: int = Field(default=1, ge=1)    
    price: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    subtotal: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)    

    # Relaciones
    invoice: Optional['Invoice'] = Relationship(back_populates="items")
    article: Optional['Article'] = Relationship()