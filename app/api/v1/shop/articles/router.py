from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_session

from .services import ArticleQueryService

from .schemas import ArticlePublicPagination, ArticlePublicResponse


router = APIRouter()

@router.get(
    '/all', 
    response_model=ArticlePublicPagination,
    status_code=status.HTTP_200_OK
)
async def get_all(  
    page_size: int = Query(default=10, ge=1, le=50),
    page: int = Query(default=1, ge=1),  
    query: Optional[str] = Query(default=None, min_length=2, max_length=50),
    brand: Optional[str] = Query(default=None, min_length=2, max_length=50),
    category: Optional[str] = Query(default=None, min_length=2, max_length=50),    
    db: AsyncSession = Depends(get_session)
) -> ArticlePublicPagination:
    article_service = ArticleQueryService(db=db)

    pagination = await article_service.get_all_pagination(
        page_size=page_size,
        page=page,
        title=query,
        brand=brand,
        category=category
    )
    return pagination


@router.get(
    '/{slug}', 
    response_model=ArticlePublicResponse, 
    status_code=status.HTTP_200_OK
)
async def get_article_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_session)   
) -> ArticlePublicResponse:
    article_service = ArticleQueryService(db=db)

    return await article_service.get_article_by_slug(slug=slug)