from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import InvoiceCreate, InvoicePublic

from app.models.users import User

from app.core.exceptions import ArticleNotFound, InsufficientInventory 
from app.core.exceptions import PaymentException, PriceMismatch

from app.utils.permission import client_dependency

from .services import CheckOutService

from app.core.db import get_session

router = APIRouter()


@router.post(
    '', 
    status_code=status.HTTP_201_CREATED, 
    response_model=InvoicePublic
)
async def create(
    data: InvoiceCreate,    
    user: User = client_dependency,
    db: AsyncSession = Depends(get_session)
) -> InvoicePublic:
    service = CheckOutService(db=db)

    try:
        invoice = await service.checkout(
            data=data,             
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