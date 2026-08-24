from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.auth.schemas import UserLogin

from app.repositories.users import UserRepository
from app.core.exceptions import CredentialsException, UserNotFound
from app.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)


    async def authentication(self, login: UserLogin) -> str:        
        try:
            user_db = await self.user_repo.get_by_email(email=login.email)
            
            if not user_db:
                raise UserNotFound()
                    
            if not verify_password(login.password, user_db.hashed_password):
                raise CredentialsException()
            
            access_token = create_access_token(
                data={"sub": user_db.email, "role": user_db.role}
            )
            return access_token
        except Exception as e:
            raise e