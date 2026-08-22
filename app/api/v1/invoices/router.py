from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Path 
from fastapi import Query, status

from app.api.v1.invoice_items.service import InvoiceItemsService

from app.api.v1.payments.schemas import CardStripe
from app.api.v1.users.models import User

from app.core.exceptions import ArticleNotFound, InsufficientInventory 
from app.core.exceptions import InvoiceNotFound, PaymentException 
from app.core.exceptions import PriceMismatch

from .enums import InvoiceSortField, InvoiceStatus
from .schemas import InvoiceCreate, InvoicePaginationResponse
from .schemas import InvoiceResponse
from .service import InvoiceService

from app.core.db import get_session

from typing import Literal, Optional
from app.utils.permission import client_dependency

router = APIRouter()


@router.get(
    '/', 
    response_model=InvoicePaginationResponse, 
    status_code=status.HTTP_200_OK
)
async def get_all(
    page_size: int = Query(default=10, ge=1, le=50),
    page: int = Query(default=1, ge=1),  
    status: Optional[InvoiceStatus] = Query(default=None, description='Filtrar por estado'),       
    client_id: Optional[int] = Query(default=None, ge=1, description='Filtrar por cliente ID'),
    full_name: Optional[str] = Query(default=None, min_length=2, max_length=60),
    sort_by: InvoiceSortField = Query(
        default=InvoiceSortField.ID, 
        description='Campo por el cual ordenar'
    ),
    sort_order: Literal['asc', 'desc'] = Query(
        default='asc', 
        description='Dirección del ordenamiento: asc o desc'
    ),
    db: AsyncSession = Depends(get_session)
) -> InvoicePaginationResponse:
    invoice_service = InvoiceService(db=db)

    pagination = await invoice_service.get_all_pagination(
        page_size=page_size,
        page=page,
        status=status,
        client_id=client_id,
        full_name=full_name,
        sort_by=sort_by,       
        sort_order=sort_order
    )
    return pagination


@router.get(
    '/{invoice_id}', 
    response_model=InvoiceResponse,
    status_code=status.HTTP_200_OK
)
async def get_invoice(
    invoice_id: int = Path(
        ..., 
        ge=1,
        description='Identificador entero de la factura, debe ser mayor o igual a 1',
        examples=[1]
    ),
    db: AsyncSession = Depends(get_session)
) -> InvoiceResponse:
    invoice_service = InvoiceService(db=db)

    try:       
        return await invoice_service.get_invoice(invoice_id=invoice_id)
    except InvoiceNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invoice not found"
        )


@router.get(
    '/{invoice_id}/items', 
    response_model=list[InvoiceResponse],
    status_code=status.HTTP_200_OK
)
async def get_items(
    invoice_id: int = Path(
        ..., 
        ge=1,
        description='Identificador entero de la factura, debe ser mayor o igual a 1',
        examples=[1]
    ),
    db: AsyncSession = Depends(get_session)
) -> InvoiceResponse:
    invoice_service = InvoiceItemsService(db=db)

    return await invoice_service.get_items(invoice_id=invoice_id)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_invoice(
    data: InvoiceCreate,
    card: CardStripe,
    user: User = client_dependency,
    db: AsyncSession = Depends(get_session)
) -> InvoiceResponse:
    invoice_service = InvoiceService(db=db)

    try:
        invoice = await invoice_service.create_invoice(
            data=data, 
            card=card, 
            user_id=user.id
        )
        return invoice
    except (
        ArticleNotFound, 
        InsufficientInventory, 
        PriceMismatch, 
        PaymentException
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Lo sentimos, no se pudo completar la compra'
        )