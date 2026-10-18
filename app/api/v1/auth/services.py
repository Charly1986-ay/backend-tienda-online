from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.users import User

from .schemas import UserLogin
from app.api.v1.users.schemas import UserCreate

from app.api.v1.users.repository import UserRepository

from app.core.exceptions import CredentialsException
from app.core.exceptions import UserExistsException, UserNotFound

from app.core.security import create_access_token
from app.core.security import get_password_hash, verify_password


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db=db)


    async def authentication(self, login: UserLogin) -> str:
        user_db = await self.user_repo.get_by_email(email=login.email)

        if not user_db:
            raise UserNotFound()

        if not verify_password(login.password, user_db.hashed_password):
            raise CredentialsException()

        access_token = create_access_token(
            data={"sub": user_db.email}
        )
        return {
            'user': user_db,
            'token': access_token            
        }


    async def register_account(self, user: UserCreate):
        user_db = await self.user_repo.get_by_email(
            email=user.email
        )
    
        if user_db:
            raise UserExistsException()
    
        user_db = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=get_password_hash(
                password=user.password
            )
        )
    
        try:           
            user_db = await self.user_repo.create(user=user_db)
    
            await self.db.commit()
            await self.db.refresh(user_db)
            return user_db
        except Exception as e:           
            await self.db.rollback()
            raise e    


    def check_status(self, email) -> str:
        return create_access_token(data={"sub": email})