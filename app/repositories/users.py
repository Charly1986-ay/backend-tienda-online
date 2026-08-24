from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.users import User


class UserRepository:    
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def get(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    
    async def get_by_email(self, email: str) -> User | None:        
        result = await self.db.exec(select(User).where(
            User.email == email)
        )        
        return result.one_or_none()

    
    async def create(self, user: User) -> User:
        self.db.add(user)        
        await self.db.flush()
        return user

    
    async def update(self, user: User, updates: dict) -> User:        
        for key, value in updates.items():
            setattr(user, key, value)
        self.db.add(user)
        await self.db.flush()
        return user