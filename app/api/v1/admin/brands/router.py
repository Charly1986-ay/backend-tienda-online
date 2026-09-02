from fastapi import APIRouter, Depends, HTTPException 
from fastapi import Path, status

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.articles.schemas import ArticleResponse

from app.api.v1.admin.brands.schemas import BrandCreate, BrandResponse
from app.models.users import User

from app.services.brand import BrandService

from app.core.db import get_session
from app.core.exceptions import BrandExistsException, BrandNotFound

from app.utils.permission import it_support_specialist


router = APIRouter()


@router.post('/insert', response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def insert_brand(
    data: BrandCreate,
    current: User = it_support_specialist,
    db: AsyncSession = Depends(get_session)
) -> BrandResponse:
    service = BrandService(db=db)
    try:
        return await service.insert_brand(data=data, user_id=current.id)

    except BrandExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No se pudo añadir la marca'
        )


@router.put('/update/{brand_id}', response_model=BrandResponse, status_code=status.HTTP_200_OK)
async def update_brand(
    brand_id: int,
    data: BrandCreate,
    current: User = it_support_specialist,
    db: AsyncSession = Depends(get_session)
) -> BrandResponse:
    service = BrandService(db=db)
    try:
        return await service.update_brand(
            data=data, 
            brand_id=brand_id,
            user_id=current.id
        )

    except (BrandExistsException, BrandNotFound):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No se pudo actualizar la marca'
        )



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