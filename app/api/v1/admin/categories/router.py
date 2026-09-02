from fastapi import APIRouter, Depends, HTTPException, Path, status


from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.articles.schemas import ArticleResponse
from app.api.v1.admin.categories.schemas import CategoryCreate, CategoryResponse

from app.models.users import User
from app.services.category import CategoryService

from app.core.db import get_session

from app.core.exceptions import CategoryExistsException, CategoryNotFound

from app.utils.permission import it_support_specialist

router = APIRouter()


@router.post('/insert', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def insert_category(
    data: CategoryCreate,
    current: User = it_support_specialist,
    db: AsyncSession = Depends(get_session)
) -> CategoryResponse:
    service = CategoryService(db=db)
    try:
        return await service.insert_category(data=data, user_id=current.id)

    except CategoryExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No se pudo añadir la categoría'
        )


@router.put('/update/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(
    category_id: int,
    data: CategoryCreate,
    current: User = it_support_specialist,
    db: AsyncSession = Depends(get_session)
) -> CategoryResponse:
    service = CategoryService(db=db)
    try:
        return await service.update_category_category(
            data=data, 
            category_id=category_id,
            user_id=current.id
        )

    except (CategoryExistsException, CategoryNotFound):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No se pudo actualizar la categoría'
        )


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