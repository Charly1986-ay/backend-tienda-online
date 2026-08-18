from enum import Enum

class InvoiceStatus(str, Enum):
    PENDING = 'pending'       #Pendiente de pago
    PAID = 'paid'             # Pagada
    VOIDED = 'voided'         # Anulada
    REFUNDED = 'refunded'     # Reembolsada


class InvoiceSortField(str, Enum):
    ID = 'id'
    NUMBER = 'number'
    FULLNAME = 'fullname'
    DATE = 'date'
    TOTAL = 'total'