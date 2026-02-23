from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class MemberCreated(DomainEvent):
    member_id: str = ""
    email: str = ""


@dataclass(frozen=True)
class MemberEmailChanged(DomainEvent):
    member_id: str = ""
    old_email: str = ""
    new_email: str = ""


@dataclass(frozen=True)
class MemberProfileUpdated(DomainEvent):
    member_id: str = ""
    name: str = ""


@dataclass(frozen=True)
class MemberPasswordChanged(DomainEvent):
    member_id: str = ""


@dataclass(frozen=True)
class MemberDeleted(DomainEvent):
    member_id: str = ""
