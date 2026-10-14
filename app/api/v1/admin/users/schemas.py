from pydantic import BaseModel, ConfigDict, EmailStr

from app.api.v1.users.enums import Role, UserStatus
from app.api.v1.auth.schemas import UserCreate

class AdminUserCreate(UserCreate):    
    role: Role = Role.CLIENT.value


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    status: UserStatus
    model_config = ConfigDict(from_attributes=True)