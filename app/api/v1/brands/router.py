from fastapi import APIRouter, Depends, HTTPException 
from fastapi import Path, status

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.articles.schemas import ArticleResponse

from .service import BrandService

from app.core.db import get_session
from app.core.exceptions import BrandNotFound


router = APIRouter()

@router.get(
    '/{brand_id}/categories', 
    response_model=list[ArticleResponse],
    status_code=status.HTTP_200_OK
)
async def get_articles_by_brand(  
    brand_id: int = Path(
        ..., 
        ge=1,
        description='Identificador entero de la marca, debe ser mayor o igual a 1',
        examples=[1]
    ),  
    db: AsyncSession = Depends(get_session)
) -> list[ArticleResponse]:
    brand_service = BrandService(db=db)

    try:
        return await brand_service.get_articles_by_brand(
            brand_id=brand_id
        )
    except BrandNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Marca no encontrada'
        ) 