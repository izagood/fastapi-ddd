from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member_validator import PasswordValidator


class CreateMemberRequest(BaseModel):
    email: EmailStr
    passwd: str
    name: str

    @field_validator("passwd")
    @classmethod
    def validate_passwd(cls, value: str) -> str:
        return PasswordValidator.validate(value)


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
        return PasswordValidator.validate(value)
