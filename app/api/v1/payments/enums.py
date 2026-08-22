from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = "refunded"


class TypeCurrency(str, Enum):
    USD = 'usd'
    EUR = 'eur'
    ARG = 'ars'