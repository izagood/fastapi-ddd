from fastapi_ddd.application.member.member_request import (
    CreateMemberRequest,
    GetMemberRequest,
    UpdateMemberProfileRequest,
)
from fastapi_ddd.application.member.member_response import (
    CreateMemberResponse,
    GetMemberResponse,
    GetMembersResponse,
    MemberDTO,
    UpdateMemberProfileResponse,
)
from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member import Member
from fastapi_ddd.infra.database.unit_of_work import UnitOfWork


class MemberService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_member(self, request: CreateMemberRequest) -> CreateMemberResponse:
        member = Member(
            email=request.email,
            passwd=request.passwd,
            name=request.name,
        )
        await self.uow.members.create(self.uow.session, member)
        await self.uow.commit()

        return CreateMemberResponse(member_dto=MemberDTO.from_member(member))

    async def get_members(self) -> GetMembersResponse:
        members = await self.uow.members.find_all(self.uow.session)

        member_dto_list = [MemberDTO.from_member(member) for member in members]

        return GetMembersResponse(member_dto_list=member_dto_list)

    async def get_member(self, request: GetMemberRequest) -> GetMemberResponse:
        member = await self.uow.members.find_by_id(self.uow.session, request.entity_id)

        return GetMemberResponse(member_dto=MemberDTO.from_member(member))

    async def update_member_profile(self, entity_id: EntityId, request: UpdateMemberProfileRequest):
        member = await self.uow.members.find_by_id(self.uow.session, entity_id)
        member.update_profile(**request.model_dump())
        await self.uow.commit()

        return UpdateMemberProfileResponse(member_dto=MemberDTO.from_member(member))

    async def delete_member(self, entity_id: EntityId):
        member = await self.uow.members.find_by_id(self.uow.session, entity_id)
        member.delete()
        await self.uow.commit()
