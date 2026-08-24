from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.models.articles import UnitsType, StatusArticle


class ArticlePublicResponse(BaseModel):
    id: int
    detail: str
    price: Decimal                  
    units_type: UnitsType
    status: StatusArticle
    image_url: Optional[str] = None
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schema de paginación para la vista pública
class ArticlePublicPaginationResponse(BaseModel):
    counter: int
    pages: int
    page: int
    page_size: int
    articles: List[ArticlePublicResponse]

    model_config = ConfigDict(from_attributes=True)