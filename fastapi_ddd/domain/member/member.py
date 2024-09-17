from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, validates

from fastapi_ddd.domain.custom_types.entity_id_type import EntityIdType
from fastapi_ddd.domain.entity import BaseWithTime, EntityId
from fastapi_ddd.domain.member.member_validator import EmailValidator, PasswordValidator


class Member(BaseWithTime):
    __tablename__ = "member"

    id: Mapped[EntityId] = mapped_column(
        "mem_id",
        EntityIdType,
        primary_key=True,
        index=True,
        default=EntityId.create,
    )
    email: Mapped[str] = mapped_column(unique=True)
    passwd: Mapped[str]
    name: Mapped[str]
    deleted: Mapped[bool] = mapped_column(default=False)

    @validates("email")
    def validate_email(self, key, email):
        return EmailValidator.validate(email)

    @validates("passwd")
    def validate_passwd(self, key, passwd):
        return PasswordValidator.validate(passwd)

    def update_profile(
        self,
        *,
        name: Optional[str] = None,
    ):
        if name:
            self.name = name

    def change_email(self, email: str):
        if email is None:
            raise TypeError("None is not allowed")

        self.email = EmailValidator.validate(email)

    def change_passwd(self, passwd: str):
        if passwd is None:
            raise TypeError("None is not allowed")

        self.passwd = PasswordValidator.validate(passwd)

    def delete(self):
        self.deleted = True
