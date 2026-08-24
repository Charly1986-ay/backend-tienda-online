from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.articles import Article

class Brand(SQLModel, table=True):
    __tablename__ = 'brand'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    slug: str = Field(unique=True, index=True)

    articles: List["Article"] = Relationship(back_populates="brand")