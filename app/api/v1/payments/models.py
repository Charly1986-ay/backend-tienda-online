from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Field, Numeric, Relationship, SQLModel

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

    amount: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(Numeric(10, 2, asdecimal=False)) # 👈 Le dice a SQLAlchemy que lo maneje como float internamente
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
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    invoice: Optional["Invoice"] = Relationship(
        back_populates="payment",
        sa_relationship_kwargs={"lazy": "selectin"}
    )