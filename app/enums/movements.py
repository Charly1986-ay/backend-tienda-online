from enum import Enum


class TargetType(str, Enum):
    """Entidades del sistema que pueden ser auditadas o tener logs."""
    ARTICLE = 'article'
    USER = 'user'
    INVOICE = 'invoice'
    BRAND = 'brand'
    CATEGORY = 'category'
    # PROVIDER = 'provider'  # Fácilmente extensible


class MovementType(str, Enum):
    """Tipos de operaciones o movimientos universales para auditoría."""
    
    # Ciclo de vida básico (Aplica para cualquier entidad)
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    
    # Cambios de estado operativos (Muy útiles para facturas, pedidos, usuarios)
    ACTIVATED = 'activated'
    DEACTIVATED = 'deactivated'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    
    # Específicos de inventario / negocio
    PRICE_UPDATE = 'price_update'
    STOCK_CHANGE = 'stock_change'
    CATEGORY_CHANGE = 'category_change'
    BRAND_CHANGE = 'brand_change'
    ARTICLE_STATUS = 'article_status'
    INVOICE_STATUS = 'invoice_status'