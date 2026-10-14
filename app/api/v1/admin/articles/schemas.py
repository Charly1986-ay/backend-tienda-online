from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic import computed_field, field_validator

from .enums import UnitsType, StatusArticle

from app.utils.security_constants import validate_no_forbidden_words
from app.utils.slug import convert_slug


class ArticleBase(BaseModel):
    """Base para validación de palabras prohibidas en campos de texto."""

    @field_validator('title', 'detail', mode='after', check_fields=False)
    @classmethod
    def check_forbidden_words(cls, value: str | None):
        if value is None:
            return value
        return validate_no_forbidden_words(value=value)


class ArticleCreate(ArticleBase):
    title: str = Field(min_length=1, max_length=50)
    detail: str | None = Field(default=None, min_length=1, max_length=255)
    stock: int = 0
    cost: Decimal = Decimal("0.00")
    price: Decimal = Decimal("0.00")
    brand_id: int = 1
    category_id: int = 1
    units_type: UnitsType = UnitsType.UNITS    
    image: str | None = 'not-photo_512.png'

    @computed_field(return_type=str)
    @property
    def slug(self) -> str:
        return convert_slug(title=self.title)
        

class ArticleUpdate(ArticleBase):
    title: str | None = Field(default=None, min_length=1, max_length=50)    
    detail: str | None = Field(default=None, min_length=1, max_length=255)
    units_type: UnitsType | None = None
    image: str | None = None    


class UpdateStock(BaseModel):    
    stock: int = Field(..., description="Unidades a añadir o quitar")


class UpdatePrice(BaseModel):  
    cost: Decimal | None = Field(default=None, ge=0)
    price: Decimal | None = Field(default=None, ge=0)


class UpdateBrand(BaseModel):
    brand_id: int  


class UpdateCategory(BaseModel):
    category_id: int


class UpdateStatus(BaseModel):
    status: StatusArticle


class ArticleResponse(BaseModel):
    id: int
    title: str 
    slug: str   
    detail: Optional[str] = None    
    stock: int    
    cost: Decimal
    price: Decimal
    brand_id: int
    category_id: int
    units_type: UnitsType
    status: StatusArticle
    image: Optional[str] = None
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ArticlePaginationResponse(BaseModel):  
    counter: int
    pages: int
    offset: int
    page: int
    page_size: int
    articles: list[ArticleResponse]  

    model_config = ConfigDict(from_attributes=True)