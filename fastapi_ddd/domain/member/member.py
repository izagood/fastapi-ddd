from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, validates

from fastapi_ddd.domain.custom_types.entity_id_type import EntityIdType
from fastapi_ddd.domain.entity import BaseWithTime, EntityId, _utcnow
from fastapi_ddd.domain.events import (
    DomainEvent,
    MemberCreated,
    MemberDeleted,
    MemberEmailChanged,
    MemberPasswordChanged,
    MemberProfileUpdated,
)
from fastapi_ddd.domain.member.member_validator import EmailValidator, PasswordHasher, PasswordValidator


class Member(BaseWithTime):
    __tablename__ = "member"

    id: Mapped[EntityId] = mapped_column(
        "mem_id",
        EntityIdType,
        primary_key=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True)
    passwd: Mapped[str]
    name: Mapped[str]
    deleted: Mapped[bool] = mapped_column(default=False)

    def __init__(self, **kwargs):
        kwargs.setdefault("id", EntityId.create())
        kwargs.setdefault("deleted", False)
        now = _utcnow()
        kwargs.setdefault("created_at", now)
        kwargs.setdefault("updated_at", now)
        self._domain_events: list[DomainEvent] = []
        super().__init__(**kwargs)
        self._add_event(MemberCreated(member_id=str(self.id), email=self.email))

    def _ensure_events(self) -> list[DomainEvent]:
        if not hasattr(self, "_domain_events"):
            self._domain_events = []
        return self._domain_events

    def _add_event(self, event: DomainEvent) -> None:
        self._ensure_events().append(event)

    @property
    def domain_events(self) -> list[DomainEvent]:
        return list(self._ensure_events())

    def clear_events(self) -> None:
        self._ensure_events().clear()

    @validates("email")
    def validate_email(self, key, email):
        return EmailValidator.validate(email)

    @validates("passwd")
    def validate_passwd(self, key, passwd):
        return PasswordValidator.validate_and_hash(passwd)

    def update_profile(
        self,
        *,
        name: Optional[str] = None,
    ):
        if name is not None:
            self.name = name
            self._add_event(MemberProfileUpdated(member_id=str(self.id), name=name))

    def change_email(self, email: str):
        old_email = self.email
        self.email = EmailValidator.validate(email)
        self._add_event(MemberEmailChanged(member_id=str(self.id), old_email=old_email, new_email=self.email))

    def change_passwd(self, passwd: str):
        self.passwd = passwd  # @validates handles hashing
        self._add_event(MemberPasswordChanged(member_id=str(self.id)))

    def verify_passwd(self, passwd: str) -> bool:
        return PasswordHasher.verify(passwd, self.passwd)

    def delete(self):
        self.deleted = True
        self._add_event(MemberDeleted(member_id=str(self.id)))
