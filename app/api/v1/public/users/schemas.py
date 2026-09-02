from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.users import UserStatus


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    full_name: str    
    status: UserStatus
    model_config = ConfigDict(from_attributes=True)