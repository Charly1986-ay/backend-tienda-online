from pydantic import BaseModel, computed_field, field_validator

from app.utils.security_constants import validate_no_forbidden_words


class BrandCreate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def check_name(cls, value: str) -> str:
        return validate_no_forbidden_words(value=value)

    @computed_field
    @property
    def slug(self) -> str:
        return '-'.join(self.name.split())


class BrandResponse(BaseModel):
    id: str
    name: str
    slug: str