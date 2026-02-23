import pytest
from sqlalchemy import select

from fastapi_ddd.domain.exceptions import DuplicateEmailException, MemberNotFoundException
from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member import Member

VALID_PASSWORD = "Test@1234"


def _create_member(email: str = "test@example.com", name: str = "Test User") -> Member:
    return Member(email=email, passwd=VALID_PASSWORD, name=name)


class TestMemberRepository:
    async def test_create_and_find_by_id(self, repository, session):
        member = _create_member()
        await repository.create(member)
        await session.commit()

        found = await repository.find_by_id(member.id)
        assert str(found.id) == str(member.id)
        assert found.email == "test@example.com"
        assert found.name == "Test User"
        assert found.deleted is False

    async def test_find_all(self, repository, session):
        await repository.create(_create_member("a@example.com", "A"))
        await repository.create(_create_member("b@example.com", "B"))
        await session.commit()

        members = await repository.find_all()
        assert len(members) == 2

    async def test_find_all_with_pagination(self, repository, session):
        for i in range(5):
            await repository.create(_create_member(f"user{i}@example.com", f"User {i}"))
        await session.commit()

        page = await repository.find_all(skip=1, limit=2)
        assert len(page) == 2

    async def test_find_by_id_not_found(self, repository):
        with pytest.raises(MemberNotFoundException):
            await repository.find_by_id(EntityId.create())

    async def test_delete_member(self, repository, session):
        member = _create_member()
        await repository.create(member)
        await session.commit()

        member.delete()
        await session.commit()

        with pytest.raises(MemberNotFoundException):
            await repository.find_by_id(member.id)

    async def test_update_profile(self, repository, session):
        member = _create_member()
        await repository.create(member)
        await session.commit()

        member.update_profile(name="Updated Name")
        await session.commit()

        found = await repository.find_by_id(member.id)
        assert found.name == "Updated Name"

    async def test_email_uniqueness(self, repository, session):
        await repository.create(_create_member("same@example.com", "A"))
        await session.commit()

        with pytest.raises(DuplicateEmailException):
            await repository.create(_create_member("same@example.com", "B"))

    async def test_find_by_email(self, repository, session):
        member = _create_member("find@example.com", "FindMe")
        await repository.create(member)
        await session.commit()

        found = await repository.find_by_email("find@example.com")
        assert found is not None
        assert found.email == "find@example.com"

    async def test_find_by_email_not_found(self, repository):
        found = await repository.find_by_email("nonexistent@example.com")
        assert found is None

    async def test_exists_by_email(self, repository, session):
        await repository.create(_create_member("exists@example.com", "Exists"))
        await session.commit()

        assert await repository.exists_by_email("exists@example.com") is True
        assert await repository.exists_by_email("nope@example.com") is False


class TestUnitOfWorkRollback:
    async def test_uow_rollback_on_exception(self, session):
        from fastapi_ddd.infra.database.unit_of_work import UnitOfWork

        member = _create_member("rollback@example.com", "Rollback User")

        with pytest.raises(RuntimeError):
            async with UnitOfWork(session) as uow:
                await uow.members.create(member)
                raise RuntimeError("Simulated error")

        # After rollback, the member should not be persisted
        result = await session.execute(select(Member).where(Member.email == "rollback@example.com"))
        assert result.scalars().first() is None
