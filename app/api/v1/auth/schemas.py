from pydantic import BaseModel, EmailStr, field_validator

from app.api.v1.users.schemas import UserResponse
from app.utils.regex_validators import clean_string_spaces


class UserLogin(BaseModel):
    email: EmailStr    
    password: str

    @field_validator('email', 'password', mode='before')
    @classmethod
    def clean_spaces(cls, value: str) -> str:
        return clean_string_spaces(value)


class AuthResponse(BaseModel):
    user: UserResponse
    token: str