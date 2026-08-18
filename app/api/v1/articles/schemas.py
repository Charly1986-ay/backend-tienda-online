from decimal import Decimal
from typing import List, Optional
from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .models import UnitsType, StatusArticle

from app.utils.security_constants import validate_no_forbidden_words


class ArticleValidatedBase(BaseModel):
    @field_validator('detail', check_fields=False)
    @classmethod
    def check_detail(cls, value: Optional[str]):
        if value is None:
            return value
        return validate_no_forbidden_words(value=value)    


class ArticleCreate(BaseModel):
    detail: str
    stock: int = 0
    stock_min: int = 1
    cost: Decimal = Decimal("0.00")
    price: Decimal = Decimal("0.00")
    brand_id: int = 1
    category_id: int = 1
    units_type: UnitsType = UnitsType.UNITS
    status: StatusArticle = StatusArticle.AVAILABLE
    image_url: str | None = None

    @classmethod
    def as_form(
        cls,
        detail: str = Form(...),
        stock: int = Form(0),
        stock_min: int = Form(1),
        cost: Decimal = Form(Decimal("0.00")),
        price: Decimal = Form(Decimal("0.00")),
        brand_id: int = Form(1),
        category_id: int = Form(1),
        units_type: UnitsType = Form(UnitsType.UNITS),
        status: StatusArticle = Form(StatusArticle.AVAILABLE),
    ):
        return cls(
            detail=detail,
            stock=stock,
            stock_min=stock_min,
            cost=cost,
            price=price,
            brand_id=brand_id,
            category_id=category_id,
            units_type=units_type,
            status=status,
            image_url=None
        )


class ArticleUpdate(ArticleValidatedBase):    
    detail: Optional[str] = None    
    stock_min: Optional[int] = None    
    units_type: Optional[UnitsType] = None    
    image_url: Optional[str] = None


class UpdateStock(BaseModel):    
    units: int = Field(..., description="Unidades a añadir o quitar")


class UpdatePrice(BaseModel):  
    cost: Optional[Decimal] = Field(default=None, ge=0)
    price: Optional[Decimal] = Field(default=None, ge=0)


class UpdateBrand(BaseModel):
    brand_id: int  


class UpdateCategory(BaseModel):
    category_id: int


class UpdateStatus(BaseModel):
    status: StatusArticle


class ArticleResponse(BaseModel):
    id: int    
    detail: str    
    stock: int
    stock_min: int
    cost: Decimal
    price: Decimal
    brand_id: int
    category_id: int
    units_type: UnitsType
    status: StatusArticle
    image_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ArticleWithRelationsResponse(ArticleResponse):
    category_name: Optional[str] = None
    brand_name: Optional[str] = None


class ArticlePaginationResponse(BaseModel):  
    counter: int
    pages: int
    offset: int
    page: int
    page_size: int
    articles: List[ArticleWithRelationsResponse]  

    model_config = ConfigDict(from_attributes=True)