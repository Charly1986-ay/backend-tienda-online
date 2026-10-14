from decimal import Decimal
from typing import Any, Literal, Optional

from fastapi import APIRouter, Depends, File, Form
from fastapi import HTTPException, UploadFile 
from fastapi import Path, Query, status

from sqlmodel.ext.asyncio.session import AsyncSession

from .enums import ArticleSortField, StatusArticle, UnitsType
from .schemas import ArticleCreate, ArticlePaginationResponse
from .schemas import UpdateBrand, UpdateCategory, UpdatePrice
from .schemas import ArticleResponse, ArticleUpdate, UpdateStatus

from .services import ArticleService
from .services_query import ArticleQueryService

from app.models.users import User
from app.core.db import get_session
from app.core.exceptions import ArticleNotFound
from app.utils.permission import support_assistant_dependency

from app.core.file_storage import save_uploaded_image


router = APIRouter()


@router.get(
    '/', 
    response_model=ArticlePaginationResponse,
    status_code=status.HTTP_200_OK
)
async def get_all(  
    page_size: int = Query(default=10, ge=1, le=50),
    page: int = Query(default=1, ge=1),  
    title: Optional[str] = Query(default=None, min_length=2, max_length=50),
    brand: Optional[str] = Query(default=None, min_length=2, max_length=50),
    category: Optional[str] = Query(default=None, min_length=2, max_length=50),    
    sort_by: ArticleSortField = Query(
        default=ArticleSortField.ID, 
        description='Campo por el cual ordenar'
    ),
    status: Literal['all', 'available', 'unavailable'] = Query(
        default='all', 
        description='Filtrado por estados de los articulos'
    ),
    sort_order: Literal['asc', 'desc'] = Query(
        default='asc', 
        description='Dirección del ordenamiento: asc o desc'
    ),
    user: User = support_assistant_dependency,
    db: AsyncSession = Depends(get_session)
) -> ArticlePaginationResponse:
    article_service = ArticleQueryService(db=db)

    pagination = await article_service.get_all_pagination(
        page_size=page_size,
        page=page,
        title=title,
        brand=brand,
        category=category,
        status=status,
        sort_by=sort_by,       
        sort_order=sort_order
    )
    return pagination


@router.get(
    '/{article_id}', 
    response_model=ArticleResponse,
    status_code=status.HTTP_200_OK
)
async def get_article_by_id(  
    article_id: int = Path(
        ..., 
        ge=1,
        description='Identificador entero del artículo, debe ser mayor o igual a 1',
        examples=[1]
    ),  
    db: AsyncSession = Depends(get_session)
) -> ArticleResponse:
    article_service = ArticleQueryService(db=db)

    try:
        return await article_service.get_article_by_id(
            article_id=article_id
        )
    except ArticleNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Articulo no encontrado'
        ) 


@router.post(
    '/insert', 
    response_model=ArticleResponse, 
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Archivo no permitido o formato inválido"},
        413: {"description": "El archivo excede el tamaño máximo permitido"}
    }
)
async def insert_article(
    title: str = Form(...),
    detail: str | None = Form(None),
    stock: int = Form(0),
    cost: Decimal = Form(Decimal("0.00")),
    price: Decimal = Form(Decimal("0.00")),
    brand_id: int = Form(1),
    category_id: int = Form(1),
    units_type: UnitsType = Form(UnitsType.UNITS),        
    image: Optional[UploadFile] = File(None),    
    user: User = support_assistant_dependency,
    db: AsyncSession = Depends(get_session)
) -> ArticleResponse:
    article_service = ArticleService(db=db)

    data = ArticleCreate(
        title=title,
        detail=detail,
        stock=stock,
        cost=cost,
        price=price,
        brand_id=brand_id,
        category_id=category_id,
        units_type=units_type,
        image=get_image_filename(image=image)
    )
    
    return await article_service.create_article(
        article=data,
        user_id=user.id
    )


@router.put(
    '/update/{article_id}', 
    response_model=ArticleResponse, 
    status_code=status.HTTP_200_OK
)
async def update_article(    
    title: str = Form(...),
    detail: str | None = Form(None),    
    units_type: UnitsType = Form(UnitsType.UNITS),        
    image: Optional[UploadFile] = File(None), 
    article_id: int = Path(
        ..., 
        ge=1,
        description='Identificador entero del artículo, debe ser mayor o igual a 1'
    ),
    user: User = support_assistant_dependency,
    db: AsyncSession = Depends(get_session)
) -> ArticleResponse:
    data = ArticleUpdate(
        title=title,
        detail=detail,        
        units_type=units_type,
        image=get_image_filename(image=image)
    )
    return await _process_article_update(db, user.id, article_id, data, 'update')


@router.patch('/{article_id}/status', response_model=ArticleResponse)
async def change_status(    
    article_id: int = Path(..., ge=1, description='Identificador entero del artículo'),
    status: StatusArticle = Query(..., description='Nuevo estado del artículo'), # <--- Aquí está el cambio
    user: User = support_assistant_dependency,
    db: AsyncSession = Depends(get_session)
) -> ArticleResponse:  
    data = UpdateStatus(status=status)  
    return await _process_article_update(db, user.id, article_id, data, 'status')


@router.patch('/{article_id}/price', response_model=ArticleResponse)
async def change_price(    
    data: UpdatePrice,    
    article_id: int = Path(..., ge=1, description='Identificador entero del artículo, debe ser mayor o igual a 1'),
    user: User = support_assistant_dependency,
    db: AsyncSession = Depends(get_session)
) -> ArticleResponse:   
    return await _process_article_update(db, user.id, article_id, data, 'price')


@router.patch('/{article_id}/brand', response_model=ArticleResponse)
async def change_brand(    
    data: UpdateBrand,    
    article_id: int = Path(..., ge=1, description='Identificador entero del artículo, debe ser mayor o igual a 1'),
    user: User = support_assistant_dependency,
    db: AsyncSession = Depends(get_session)
) -> ArticleResponse:    
    return await _process_article_update(db, user.id, article_id, data, 'brand')


@router.patch('/{article_id}/category', response_model=ArticleResponse)
async def change_category(    
    data: UpdateCategory,    
    article_id: int = Path(..., ge=1, description='Identificador entero del artículo, debe ser mayor o igual a 1'),
    user: User = support_assistant_dependency,
    db: AsyncSession = Depends(get_session)
) -> ArticleResponse:    
    return await _process_article_update(db, user.id, article_id, data, 'category')


async def _process_article_update(
    db: AsyncSession, 
    user_id: int,
    article_id: int,
    data: Any,
    operation: str
) -> ArticleResponse:
    article_service = ArticleService(db=db)
    
    try:
        match operation:
            case 'status':
                return await article_service.change_status(data=data, article_id=article_id, user_id=user_id)
            case 'price':
                return await article_service.change_price(data=data, article_id=article_id, user_id=user_id)
            case 'brand':
                return await article_service.change_brand(data=data, article_id=article_id, user_id=user_id)
            case 'category':
                return await article_service.change_category(data=data, article_id=article_id, user_id=user_id)
            case 'update':
                return await article_service.update_article(data=data, article_id=article_id, user_id=user_id)
            case _:
                raise ValueError(f"Operación no válida: {operation}")                
    except ArticleNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Articulo no encontrado'
        )


def get_image_filename(image: UploadFile | None):
    if image and image.filename:
        saved = save_uploaded_image(image)
        return saved['filename']   
    return None