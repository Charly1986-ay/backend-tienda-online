from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import UserCreate, UserLogin
from .schemas import TokenResponse, UserPublic

from .services import AuthService

from app.core.exceptions import CredentialsException
from app.core.exceptions import UserExistsException
from app.core.exceptions import UserNotFound

from app.core.db import get_session
from app.utils.permission import get_current_user_active


router = APIRouter()


@router.get('/me', response_model=UserPublic)
async def get_profile(
    user = Depends(get_current_user_active)
) -> UserPublic:
    return user


@router.post(
    '/login', 
    response_model=TokenResponse, 
    status_code=status.HTTP_200_OK
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_session)
) -> TokenResponse:
    try:                
        auth_service = AuthService(db=db)
        token = await auth_service.authentication(login=login_data)
        
        return TokenResponse(
            access_token=token
        )
    except (UserNotFound, CredentialsException):        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales no válidas'
        )


@router.post(
    '/register', 
    response_model=UserPublic, 
    status_code=status.HTTP_201_CREATED
)
async def register_account(
    user: UserCreate,    
    db: AsyncSession = Depends(get_session)
) -> UserPublic:
    service = AuthService(db=db)

    try:
        return await service.register_account(user=user)
    except UserExistsException:
        raise HTTPException(
            detail='No se pudo registrar la cuenta',
            status_code=status.HTTP_400_BAD_REQUEST
        )