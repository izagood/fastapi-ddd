from loguru import logger

from fastapi_ddd.application.member.member_request import (
    ChangeEmailRequest,
    ChangePasswdRequest,
    CreateMemberRequest,
    GetMemberRequest,
    UpdateMemberProfileRequest,
)
from fastapi_ddd.application.member.member_response import MemberDTO
from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member import Member
from fastapi_ddd.domain.member.member_domain_service import MemberDomainService
from fastapi_ddd.application.ports.unit_of_work import AbstractUnitOfWork
from fastapi_ddd.domain.member.value_objects import Email


class MemberService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
        self._domain_service = MemberDomainService(uow.members)

    async def create_member(self, request: CreateMemberRequest) -> MemberDTO:
        email = Email(request.email)
        await self._domain_service.ensure_email_unique(email)

        member = Member(
            email=email.value,
            passwd=request.passwd,
            name=request.name,
        )
        await self.uow.members.create(member)
        await self.uow.commit()
        self._publish_events(member)

        return MemberDTO.from_member(member)

    async def get_members(self) -> list[MemberDTO]:
        members = await self.uow.members.find_all()
        return [MemberDTO.from_member(member) for member in members]

    async def get_member(self, request: GetMemberRequest) -> MemberDTO:
        member = await self.uow.members.find_by_id(request.entity_id)
        return MemberDTO.from_member(member)

    async def update_member_profile(self, entity_id: EntityId, request: UpdateMemberProfileRequest) -> MemberDTO:
        member = await self.uow.members.find_by_id(entity_id)
        member.update_profile(**request.model_dump())
        await self.uow.commit()
        await self.uow.refresh(member)
        self._publish_events(member)

        return MemberDTO.from_member(member)

    async def change_password(self, entity_id: EntityId, request: ChangePasswdRequest) -> MemberDTO:
        member = await self.uow.members.find_by_id(entity_id)
        member.change_passwd(request.passwd)
        await self.uow.commit()
        await self.uow.refresh(member)
        self._publish_events(member)

        return MemberDTO.from_member(member)

    async def change_email(self, entity_id: EntityId, request: ChangeEmailRequest) -> MemberDTO:
        email = Email(request.email)
        await self._domain_service.ensure_email_unique(email)

        member = await self.uow.members.find_by_id(entity_id)
        member.change_email(email.value)
        await self.uow.commit()
        await self.uow.refresh(member)
        self._publish_events(member)

        return MemberDTO.from_member(member)

    async def delete_member(self, entity_id: EntityId) -> None:
        member = await self.uow.members.find_by_id(entity_id)
        member.delete()
        await self.uow.commit()
        self._publish_events(member)

    def _publish_events(self, member: Member) -> None:
        for event in member.domain_events:
            logger.info(f"Domain event published: {event}")
        member.clear_events()
