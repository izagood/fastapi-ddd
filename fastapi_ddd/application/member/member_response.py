from datetime import datetime

from pydantic import BaseModel

from fastapi_ddd.domain.member.member import Member


class MemberDTO(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_member(cls, member: Member):
        return cls(
            id=str(member.id),
            email=member.email,
            name=member.name,
            created_at=member.created_at,
            updated_at=member.updated_at,
        )
