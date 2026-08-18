from decimal import Decimal
from typing import Optional
from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.api.v1.articles.enums import StatusArticle, UnitsType
from app.api.v1.categories.models import Category
from app.api.v1.brands.models import Brand


class Article(SQLModel, table=True):
    __tablename__ = 'article'
    __table_args__ = {'extend_existing': True}    
    id: Optional[int] = Field(default=None, primary_key=True)    
    detail: Optional[str]   
    stock: int = Field(default=1, ge=0) 
    stock_min: int = Field(default=1, ge=0)
    cost: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    price: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)   
    # Nuevas llaves foráneas
    brand_id: int = Field(default=1, foreign_key='brand.id', index=True)
    category_id: int = Field(default=1, foreign_key='category.id', index=True) 
    units_type: str = Field(default=UnitsType.UNITS.value, sa_column=Column(String))
    status: str = Field(default=StatusArticle.AVAILABLE.value, sa_column=Column(String))
    image_url: Optional[str] = Field(default=None)    

    # Relaciones para navegar fácilmente entre objetos en SQLAlchemy
    brand: Optional[Brand] = Relationship(back_populates="articles")
    category: Optional[Category] = Relationship(back_populates="articles")