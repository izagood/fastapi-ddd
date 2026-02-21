from unittest.mock import AsyncMock

import pytest

from fastapi_ddd.application.member.member_request import CreateMemberRequest, GetMemberRequest, UpdateMemberProfileRequest
from fastapi_ddd.application.member.member_service import MemberService
from fastapi_ddd.common.exception.custom_exceptions import DatabaseIdNotFoundException
from fastapi_ddd.domain.entity import EntityId

VALID_PASSWORD = "Test@1234"


@pytest.fixture
def member_service(mock_uow):
    return MemberService(mock_uow)


class TestCreateMember:
    async def test_create_member_success(self, member_service, mock_uow):
        mock_uow.members.create = AsyncMock()
        mock_uow.commit = AsyncMock()

        request = CreateMemberRequest(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        response = await member_service.create_member(request)

        assert response.member_dto.email == "test@example.com"
        assert response.member_dto.name == "Test User"
        mock_uow.members.create.assert_awaited_once()
        mock_uow.commit.assert_awaited_once()


class TestGetMembers:
    async def test_get_members_returns_list(self, member_service, mock_uow, sample_member):
        mock_uow.members.find_all = AsyncMock(return_value=[sample_member])

        response = await member_service.get_members()

        assert len(response.member_dto_list) == 1
        assert response.member_dto_list[0].email == "test@example.com"


class TestGetMember:
    async def test_get_member_success(self, member_service, mock_uow, sample_member):
        mock_uow.members.find_by_id = AsyncMock(return_value=sample_member)

        request = GetMemberRequest(entity_id=sample_member.id)
        response = await member_service.get_member(request)

        assert response.member_dto.email == "test@example.com"

    async def test_get_member_not_found(self, member_service, mock_uow):
        mock_uow.members.find_by_id = AsyncMock(side_effect=DatabaseIdNotFoundException())

        request = GetMemberRequest(entity_id=EntityId.create())

        with pytest.raises(DatabaseIdNotFoundException):
            await member_service.get_member(request)


class TestUpdateMemberProfile:
    async def test_update_member_profile(self, member_service, mock_uow, sample_member):
        mock_uow.members.find_by_id = AsyncMock(return_value=sample_member)
        mock_uow.commit = AsyncMock()

        request = UpdateMemberProfileRequest(name="Updated Name")
        response = await member_service.update_member_profile(sample_member.id, request)

        assert response.member_dto.name == "Updated Name"
        mock_uow.commit.assert_awaited_once()


class TestDeleteMember:
    async def test_delete_member(self, member_service, mock_uow, sample_member):
        mock_uow.members.find_by_id = AsyncMock(return_value=sample_member)
        mock_uow.commit = AsyncMock()

        await member_service.delete_member(sample_member.id)

        assert sample_member.deleted is True
        mock_uow.commit.assert_awaited_once()
