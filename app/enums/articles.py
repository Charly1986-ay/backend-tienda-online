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
    TITLE = "title"
    BRAND = "marca"
    CATEGORY = "categoria"