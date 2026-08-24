from enum import Enum


class UnitsType(str, Enum):
    UNITS = 'units'
    LITER = 'liter'
    GRAM = 'gram'
    METRO = 'metro' 


class StatusArticle(str, Enum):
    AVAILABLE = 'available'   
    UNAVAILABLE = 'unavailable'


class ArticleSortField(str, Enum):
    ID = "id"
    DETAIL = "detalle"
    BRAND = "marca"
    CATEGORY = "categoria"