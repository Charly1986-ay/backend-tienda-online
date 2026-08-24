from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.users import User
from app.repositories.users import UserRepository

from app.api.v1.admin.users.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.core.exceptions import UserExistsException, UserNotFound

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserRepository(db=db)


    async def create_user(self, user: UserCreate):
        user_db = await self.repository.get_by_email(
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
        return await self.repository.create(user=user_db)


    async def update_user(self, user_id: int, user: UserUpdate):        
        user_db = await self.repository.get(user_id=user_id)

        if not user_db:
            UserNotFound()
        
        user_dict = user.model_dump(exclude_unset=True)
        
        if "password" in user_dict:
            user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

        return await self.repository.update(user=user_db, updates=user_dict)