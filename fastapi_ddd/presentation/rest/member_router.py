from typing import Annotated, AsyncGenerator

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ddd.application.member.member_request import (
    CreateMemberRequest,
    GetMemberRequest,
    UpdateMemberProfileRequest,
)
from fastapi_ddd.application.member.member_response import MemberDTO
from fastapi_ddd.application.member.member_service import MemberService
from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.infra.database.init_db import db
from fastapi_ddd.infra.database.unit_of_work import UnitOfWork

router = APIRouter()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = db.session_maker()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_uow(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(session) as uow:
        yield uow


async def get_member_service(uow: UnitOfWork = Depends(get_uow)) -> MemberService:
    return MemberService(uow)


MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]


@router.post("/")
async def create_member(request: CreateMemberRequest, service: MemberServiceDep) -> MemberDTO:
    response = await service.create_member(request)
    return response.member_dto


@router.get("/")
async def get_members(service: MemberServiceDep) -> list[MemberDTO]:
    response = await service.get_members()
    return response.member_dto_list


@router.get("/{member_id}")
async def get_member(member_id: str, service: MemberServiceDep) -> MemberDTO:
    request = GetMemberRequest(entity_id=EntityId.of(member_id))
    response = await service.get_member(request)
    return response.member_dto


@router.patch("/{member_id}")
async def update_member_profile(
    member_id: str, request: UpdateMemberProfileRequest, service: MemberServiceDep
) -> MemberDTO:
    response = await service.update_member_profile(EntityId.of(member_id), request)
    return response.member_dto


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: str, service: MemberServiceDep):
    await service.delete_member(EntityId.of(member_id))
