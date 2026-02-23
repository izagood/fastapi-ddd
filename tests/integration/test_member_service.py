import bcrypt

from fastapi_ddd.application.member.member_request import CreateMemberRequest, GetMemberRequest
from fastapi_ddd.application.member.member_service import MemberService

VALID_PASSWORD = "Test@1234"


def _create_request(email: str = "test@example.com", name: str = "Test User") -> CreateMemberRequest:
    return CreateMemberRequest(email=email, passwd=VALID_PASSWORD, name=name)


class TestMemberServiceIntegration:
    async def test_create_member_service(self, uow, session):
        service = MemberService(uow)
        dto = await service.create_member(_create_request())

        assert dto.email == "test@example.com"
        assert dto.name == "Test User"
        assert dto.id is not None

    async def test_get_member_service(self, uow, session):
        service = MemberService(uow)
        created = await service.create_member(_create_request())

        from fastapi_ddd.domain.entity import EntityId

        request = GetMemberRequest(entity_id=EntityId.of(created.id))
        fetched = await service.get_member(request)

        assert fetched.email == created.email
        assert fetched.id == created.id

    async def test_get_all_members_service(self, uow, session):
        service = MemberService(uow)
        await service.create_member(_create_request("a@example.com", "A"))
        await service.create_member(_create_request("b@example.com", "B"))

        members = await service.get_members()
        assert len(members) == 2

    async def test_password_hashed_in_db(self, uow, session):
        service = MemberService(uow)
        await service.create_member(_create_request())

        from fastapi_ddd.domain.member.member import Member
        from sqlalchemy import select

        result = await session.execute(select(Member))
        member = result.scalars().first()
        assert member is not None
        assert member.passwd != VALID_PASSWORD
        assert bcrypt.checkpw(VALID_PASSWORD.encode("utf-8"), member.passwd.encode("utf-8"))
