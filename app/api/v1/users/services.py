from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.users import User

from app.api.v1.users.repository import UserRepository

from app.api.v1.users.schemas import UserUpdate, UserUpdateStatus


from app.core.security import get_password_hash
from app.core.exceptions import UserExistsException, UserNotFound

from app.api.v1.admin.movements.services import ActivityLogService



class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db=db)
        self.activity_log = ActivityLogService(db=db)

    
    async def update_user(
        self, 
        user_id: int, 
        user: UserUpdate        
    ) -> User:
        user_db = await self.user_repo.get(user_id=user_id)

        if not user_db:
            raise UserNotFound()

        # Validar si el email ya existe en OTRO usuario
        if user.email:
            email_validate = await self.user_repo.get_by_email(email=user.email)
            if email_validate and email_validate.id != user_id:
                raise UserExistsException()
        
        user_dict = user.model_dump(exclude_unset=True)
        
        if "password" in user_dict:
            user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

        try:
            user_response = await self.user_repo.update(
                user=user_db, 
                updates=user_dict
            )            

            await self.db.commit()
            await self.db.refresh(user_response)

            return user_response
        except Exception as e:
            await self.db.rollback()
            raise e


    async def deactivate_account(
        self, 
        user_id: int, 
        user: UserUpdateStatus
    ) -> User:
        user_db = await self.user_repo.get(user_id=user_id)

        if not user_db:
            raise UserNotFound()

        user_dict = user.model_dump(exclude_unset=True)        

        try:
            user_response = await self.user_repo.update(
                user=user_db, 
                updates=user_dict
            )            

            await self.db.commit()
            await self.db.refresh(user_response)
            return user_response
        except Exception as e:
            await self.db.rollback()
            raise e