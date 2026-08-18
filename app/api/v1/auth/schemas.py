from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from app.api.v1.users.models import Role

class UserLogin(BaseModel):
    email: EmailStr    
    password: str

    @field_validator('email', 'password', mode='before')
    @classmethod
    def clean_spaces(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


class UserPublic(BaseModel):
    email: EmailStr
    full_name: str
    role: Role

    model_config = ConfigDict(from_attributes=True)
    

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"