import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.api.v1.payments.enums import PaymentStatus, TypeCurrency


if TYPE_CHECKING:   
    from app.api.v1.invoices.models import Invoice


class Payment(SQLModel, table=True):
    __tablename__ = "payment"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    invoice_id: int = Field(
        foreign_key="invoice.id",
        unique=True,
        index=True
    )

    # Dinero expresado en la unidad mínima de la moneda
    # Ej: $920.00 -> 92000
    amount: int = Field(
        default=0,
        ge=0
    )

    currency: str = Field(
        default=TypeCurrency.USD.value
    )

    stripe_payment_intent_id: Optional[str] = Field(
        default=None,
        unique=True,
        index=True
    )

    status: str = Field(
        default=PaymentStatus.PENDING.value
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(datetime.timezone.utc),
        nullable=False
    )

    # Relación con Invoice
    invoice: Optional["Invoice"] = Relationship(
        back_populates="payment",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
