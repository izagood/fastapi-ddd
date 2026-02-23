from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from fastapi_ddd.domain.entity import EntityId


class CreateMemberRequest(BaseModel):
    email: EmailStr
    passwd: str
    name: str

    @field_validator("passwd")
    @classmethod
    def validate_passwd(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("passwd must be at least 8 characters")
        return value


class GetMemberRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    entity_id: EntityId


class UpdateMemberProfileRequest(BaseModel):
    name: Optional[str]


class ChangePasswdRequest(BaseModel):
    passwd: str

    @field_validator("passwd")
    @classmethod
    def validate_passwd(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("passwd must be at least 8 characters")
        return value


class ChangeEmailRequest(BaseModel):
    email: EmailStr
