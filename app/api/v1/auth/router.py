from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.users import User

from app.api.v1.users.schemas import UserCreate, UserResponse
from .schemas import AuthResponse, UserLogin

from .services import AuthService

from app.core.exceptions import CredentialsException
from app.core.exceptions import UserExistsException
from app.core.exceptions import UserNotFound

from app.core.db import get_session

from app.utils.permission import get_current_user_active


router = APIRouter()


# Renovación automática de Token, si el mismo no expiro y es válido
@router.get('/check-status')
def check_token_status(
    current_user: User = Depends(get_current_user_active),
    db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    auth_service = AuthService(db=db)
    return {
        'user': current_user,
        'token': auth_service.check_status(
            current_user.email
        )
    }


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=AuthResponse
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    try:        
        auth_service = AuthService(db=db)
        user_dict = await auth_service.authentication(
            login=login_data
        )
        return user_dict

    except (UserNotFound, CredentialsException):        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales no válidas',
            headers={"WWW-Authenticate": "Bearer"}, # Recomendado para APIs basadas en tokens
        )


@router.post(
    '/register', 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED
)
async def register_account(
    user: UserCreate,    
    db: AsyncSession = Depends(get_session)
) -> UserResponse:
    service = AuthService(db=db)

    try:
        return await service.register_account(user=user)
    except UserExistsException:
        raise HTTPException(
            detail='No se pudo registrar la cuenta',
            status_code=status.HTTP_400_BAD_REQUEST
        )