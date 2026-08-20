from fastapi import APIRouter, Depends, HTTPException, Path, status


from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.articles.schemas import ArticleResponse
from app.api.v1.categories.service import CategoryService
from app.core.db import get_session
from app.core.exceptions import CategoryNotFound


router = APIRouter()


@router.get(
    '/{category_id}/articles', 
    response_model=list[ArticleResponse],
    status_code=status.HTTP_200_OK
)
async def get_articles_by_category(  
    category_id: int = Path(
        ..., 
        ge=1,
        description='Identificador entero de la categoría, debe ser mayor o igual a 1',
        examples=[1]
    ),  
    db: AsyncSession = Depends(get_session)
) -> list[ArticleResponse]:
    article_service = CategoryService(db=db)

    try:
        return await article_service.get_articles_by_category(
            category_id=category_id
        )
    except CategoryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Categoría no encontrada'
        )