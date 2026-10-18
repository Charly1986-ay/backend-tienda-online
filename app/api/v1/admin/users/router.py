from fastapi import APIRouter, Depends, HTTPException, status

from app.core.db import get_session

from app.core.exceptions import UserExistsException, UserNotFound
from app.utils.permission import it_support_specialist, client_dependency

from app.models.users import User

from .schemas import AdminUserCreate

from app.api.v1.users.schemas import UserResponse
from app.api.v1.users.schemas import UserUpdate, UserUpdateStatus

from .services import AdminUserService

from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()


@router.post(
    '/register', 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED
)
async def register(
    user: AdminUserCreate,
    current: User = it_support_specialist,
    db: AsyncSession = Depends(get_session)
) -> UserResponse:
    service = AdminUserService(db=db)

    try:
        return await service.register_account(user=user, admin=current)
    except UserExistsException:
        raise HTTPException(
            detail='No se pudo registrar el usuario',
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.put(
    '/update',
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK
)
async def update_account(    
    user: UserUpdate,    
    current: User = client_dependency,
    db: AsyncSession = Depends(get_session)
) -> UserResponse:
    service = AdminUserService(db=db)

    try:
        return await service.update_user(
            user_id=current.id,
            user=user
        )
    except (UserNotFound, UserExistsException):
        raise HTTPException(
            detail='No se pudo actualizar la cuenta',
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.patch(
    '/deactivate/{user_id}',
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK
)
async def deactivate(
    user_id: int,
    user: UserUpdateStatus,    
    current: User = it_support_specialist,
    db: AsyncSession = Depends(get_session)
) -> UserResponse:
    service = AdminUserService(db=db)

    try:
        return await service.deactivate_account(
            user_id=user_id, 
            user=user, 
            admin=current
        )
    except UserNotFound:
        raise HTTPException(
            detail='No se pudo desactivar la cuenta',
            status_code=status.HTTP_400_BAD_REQUEST
        )