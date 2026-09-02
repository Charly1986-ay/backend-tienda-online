from fastapi import APIRouter, Depends, HTTPException, status

from app.core.db import get_session

from app.core.exceptions import UserExistsException, UserNotFound

from app.enums.users import Role

from app.models.users import User
from app.utils.permission import client_dependency

from app.api.v1.admin.users.schemas import UserCreate, UserUpdate, UserUpdateStatus
from .schemas import UserPublic

from app.services.users import UserService

from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()

@router.post('/register-account', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_account(
    user: UserCreate,    
    db: AsyncSession = Depends(get_session)
) -> UserPublic:
    service = UserService(db=db)

    try:
        user_data = user.model_copy(update={'role': Role.CLIENT.value})

        return await service.register_account(user=user_data)
    except UserExistsException:
        raise HTTPException(
            detail='No se pudo registrar la cuenta',
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.put(
    '/update-account',
    response_model=UserPublic, 
    status_code=status.HTTP_200_OK
)
async def update_account(    
    user: UserUpdate,    
    current: User = client_dependency,
    db: AsyncSession = Depends(get_session)
) -> UserPublic:
    service = UserService(db=db)

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
    '/deactivate-account', 
    response_model=UserPublic, 
    status_code=status.HTTP_200_OK
)
async def deactivate(   
    user: UserUpdateStatus,    
    current: User = client_dependency,
    db: AsyncSession = Depends(get_session)
) -> UserPublic:
    service = UserService(db=db)

    try:
        return await service.deactivate_account(
            user_id=current.id, 
            user=user            
        )
    except UserNotFound:
        raise HTTPException(
            detail='No se pudo desactivar la cuenta',
            status_code=status.HTTP_400_BAD_REQUEST
        )