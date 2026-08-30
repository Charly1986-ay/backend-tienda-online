from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query, status

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_session
from app.enums.articles import ArticleSortField
from app.services.article import ArticleService

from .schemas import ArticlePublicPagination


router = APIRouter()

@router.get(
    '/all', 
    response_model=ArticlePublicPagination,
    status_code=status.HTTP_200_OK
)
async def get_all(  
    page_size: int = Query(default=10, ge=1, le=50),
    page: int = Query(default=1, ge=1),  
    detail: Optional[str] = Query(default=None, min_length=2, max_length=50),
    brand: Optional[str] = Query(default=None, min_length=2, max_length=50),
    category: Optional[str] = Query(default=None, min_length=2, max_length=50),    
    sort_by: ArticleSortField = Query(
        default=ArticleSortField.ID, 
        description='Campo por el cual ordenar'
    ),    
    sort_order: Literal['asc', 'desc'] = Query(
        default='asc', 
        description='Dirección del ordenamiento: asc o desc'
    ),
    db: AsyncSession = Depends(get_session)
) -> ArticlePublicPagination:
    article_service = ArticleService(db=db)

    pagination = await article_service.get_all_pagination(
        page_size=page_size,
        page=page,
        detail=detail,
        brand=brand,
        category=category,
        status='available',
        sort_by=sort_by,       
        sort_order=sort_order
    )
    return pagination