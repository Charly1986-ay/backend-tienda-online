from app.api.v1.users.enums import Role
from app.api.v1.users.schemas import UserCreate

class AdminUserCreate(UserCreate):    
    role: Role