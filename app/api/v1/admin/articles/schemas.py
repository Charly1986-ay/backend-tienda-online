from decimal import Decimal
from typing import List, Optional
from fastapi import File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from app.core.file_storage import save_uploaded_image
from app.models.articles import UnitsType, StatusArticle

from app.utils.security_constants import validate_no_forbidden_words


class ArticleValidationMixin(BaseModel):
    """Mixin para compartir la validación de palabras prohibidas en campos de texto."""

    @field_validator('title', 'detail', mode='after', check_fields=False)
    @classmethod
    def check_forbidden_words(cls, value: Optional[str]):
        if value is None:
            return value
        return validate_no_forbidden_words(value=value)


class ArticleBase(ArticleValidationMixin):
    title: str = Field(min_length=1, max_length=50)
    detail: str | None = Field(default=None, min_length=1, max_length=255)


class ArticleCreate(ArticleBase):
    stock: int = 0
    cost: Decimal = Decimal("0.00")
    price: Decimal = Decimal("0.00")
    brand_id: int = 1
    category_id: int = 1
    units_type: UnitsType = UnitsType.UNITS    
    image_url: str | None = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        detail: str | None = Form(None),
        stock: int = Form(0),
        cost: Decimal = Form(Decimal("0.00")),
        price: Decimal = Form(Decimal("0.00")),
        brand_id: int = Form(1),
        category_id: int = Form(1),
        units_type: UnitsType = Form(UnitsType.UNITS),       
        image: Optional[UploadFile] = File(None),
    ):
        image_url = '/not-photo_512.png'
        if image and image.filename:
            image_url = save_uploaded_image(image)['url']

        try:
            return cls(
                title=title, 
                detail=detail, 
                stock=stock,
                cost=cost, 
                price=price, 
                brand_id=brand_id,
                category_id=category_id, 
                units_type=units_type,
                image_url=image_url
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]
            )


class ArticleUpdate(ArticleValidationMixin):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    detail: str | None = Field(default=None, min_length=1, max_length=255)
    units_type: UnitsType | None = None
    image_url: str | None = None

    @classmethod
    def as_form(
        cls,
        title: str | None = Form(None),
        detail: str | None = Form(None),
        units_type: UnitsType | None = Form(None),
        image: Optional[UploadFile] = File(None),
    ):
        # Creamos un diccionario base solo con los campos que sí llegaron
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if detail is not None:
            update_data["detail"] = detail
        if units_type is not None:
            update_data["units_type"] = units_type

        # Solo si hay una imagen nueva la procesamos y la agregamos
        if image and image.filename:
            saved = save_uploaded_image(image)
            update_data["image_url"] = saved['url']

        try:
            return cls(**update_data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]
            )


class UpdateStock(BaseModel):    
    stock: int = Field(..., description="Unidades a añadir o quitar")

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
    title: str    
    detail: Optional[str] = None    
    stock: int    
    cost: Decimal
    price: Decimal
    brand_id: int
    category_id: int
    units_type: UnitsType
    status: StatusArticle
    image_url: Optional[str] = None
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ArticlePaginationResponse(BaseModel):  
    counter: int
    pages: int
    offset: int
    page: int
    page_size: int
    articles: List[ArticleResponse]  

    model_config = ConfigDict(from_attributes=True)