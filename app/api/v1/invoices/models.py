from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from sqlmodel import Column, Field, Relationship, SQLModel, String

from .enums import InvoiceStatus


if TYPE_CHECKING:
    from app.api.v1.invoice_items.models import InvoiceItem
    from app.api.v1.payments.models import Payment
    from app.api.v1.users.models import User


class Invoice(SQLModel, table=True):
    __tablename__ = 'invoice'
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)

    client_id: int = Field(foreign_key='user.id', nullable=False, index=True)
    
    # Opcional al crear en código, pero único en la base de datos
    invoice_number: Optional[str] = Field(default=None, unique=True, index=True)
    
    date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    total: Decimal = Field(default=Decimal('0.00'), ge=0, decimal_places=2)
    status: InvoiceStatus = Field(default=InvoiceStatus.PAID.value, sa_column=Column(String))

    # Relación bidireccional con los ítems de la factura
    items: list['InvoiceItem'] = Relationship(
        back_populates='invoice',
        sa_relationship_kwargs={'lazy': 'selectin'}
    )
    # Relación con el modelo User (el cliente)
    client: Optional['User'] = Relationship(
        back_populates='invoices',
        sa_relationship_kwargs={'lazy': 'selectin'}
    )
    payment: Optional['Payment'] = Relationship(back_populates='invoice')


    @property
    def fullname(self) -> Optional[str]:
        '''Calcula el full_name a partir de la relación User'''
        return self.client.full_name if self.client else None