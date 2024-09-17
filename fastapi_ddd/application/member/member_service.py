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
from fastapi_ddd.domain.member.member_repository import MemberRepository
from fastapi_ddd.infra.database.database import Database


class MemberService:
    def __init__(self):
        self.database = Database()
        self.repository = MemberRepository()

    async def create_member(self, request: CreateMemberRequest) -> CreateMemberResponse:
        with self.database.session_factory() as session:
            member = Member(
                email=request.email,
                passwd=request.passwd,
                name=request.name,
                type_code=request.type_code,
                auth=request.auth,
            )
            self.repository.create(session, member)

        return CreateMemberResponse(member_dto=MemberDTO.from_member(member))

    async def get_members(self) -> GetMembersResponse:
        with self.database.session_factory() as session:
            members = self.repository.find_all(session)

            member_dto_list: list[MemberDTO] = []

            for member in members:
                member_dto_list.append(MemberDTO.from_member(member))

        return GetMembersResponse(member_dto_list=member_dto_list)

    async def get_member(self, request: GetMemberRequest) -> GetMemberResponse:
        with self.database.session_factory() as session:
            member = self.repository.find_by_id(session, request.entity_id)

        return GetMemberResponse(member_dto=MemberDTO.from_member(member))

    async def update_member_profile(self, entity_id: EntityId, request: UpdateMemberProfileRequest):
        with self.database.session_factory() as session:
            member = self.repository.find_by_id(session, entity_id)
            member.update_profile(**request.model_dump())

        return UpdateMemberProfileResponse(member_dto=MemberDTO.from_member(member))

    async def delete_member(self, entity_id: EntityId):
        with self.database.session_factory() as session:
            member = self.repository.find_by_id(session, entity_id)
            member.delete()
