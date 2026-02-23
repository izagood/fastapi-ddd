from typing import Annotated

from fastapi import APIRouter, Depends, status

from fastapi_ddd.application.member.member_request import (
    ChangeEmailRequest,
    ChangePasswdRequest,
    CreateMemberRequest,
    GetMemberRequest,
    UpdateMemberProfileRequest,
)
from fastapi_ddd.application.member.member_response import MemberDTO
from fastapi_ddd.application.member.member_service import MemberService
from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.infra.dependencies import get_member_service

router = APIRouter()

MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_member(request: CreateMemberRequest, service: MemberServiceDep) -> MemberDTO:
    return await service.create_member(request)


@router.get("/")
async def get_members(service: MemberServiceDep) -> list[MemberDTO]:
    return await service.get_members()


@router.get("/{member_id}")
async def get_member(member_id: str, service: MemberServiceDep) -> MemberDTO:
    request = GetMemberRequest(entity_id=EntityId.of(member_id))
    return await service.get_member(request)


@router.patch("/{member_id}")
async def update_member_profile(
    member_id: str, request: UpdateMemberProfileRequest, service: MemberServiceDep
) -> MemberDTO:
    return await service.update_member_profile(EntityId.of(member_id), request)


@router.patch("/{member_id}/email")
async def change_email(member_id: str, request: ChangeEmailRequest, service: MemberServiceDep) -> MemberDTO:
    return await service.change_email(EntityId.of(member_id), request)


@router.patch("/{member_id}/password")
async def change_password(member_id: str, request: ChangePasswdRequest, service: MemberServiceDep) -> MemberDTO:
    return await service.change_password(EntityId.of(member_id), request)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: str, service: MemberServiceDep):
    await service.delete_member(EntityId.of(member_id))
