from typing import Annotated

from fastapi import APIRouter, Depends, status

from fastapi_ddd.application.member.member_request import (
    CreateMemberRequest,
    GetMemberRequest,
    UpdateMemberProfileRequest,
)
from fastapi_ddd.application.member.member_response import MemberDTO
from fastapi_ddd.application.member.member_service import MemberService
from fastapi_ddd.domain.entity import EntityId

router = APIRouter()

member_service = Annotated[MemberService, Depends(MemberService)]


@router.post("/")
async def create_member(request: CreateMemberRequest, member_service: member_service) -> MemberDTO:
    response = await member_service.create_member(request)
    return response.member_dto


@router.get("/")
async def get_members(member_service: member_service) -> list[MemberDTO]:
    response = await member_service.get_members()
    return response.member_dto_list


@router.get("/{member_id}")
async def get_member(member_id: str, member_service: member_service) -> MemberDTO:
    request = GetMemberRequest(entity_id=EntityId.of(member_id))
    response = await member_service.get_member(request)
    return response.member_dto


@router.patch("/{member_id}")
async def update_member_profile(
    member_id: str, request: UpdateMemberProfileRequest, member_service: member_service
) -> MemberDTO:
    response = await member_service.update_member_profile(EntityId.of(member_id), request)
    return response.member_dto


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: str, member_service: member_service):
    await member_service.delete_member(EntityId.of(member_id))
