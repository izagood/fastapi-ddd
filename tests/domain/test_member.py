import pytest

from fastapi_ddd.domain.entity import EntityId
from fastapi_ddd.domain.member.member import Member


VALID_PASSWORD = "Test@1234"


class TestEntityId:
    def test_create_generates_unique_ids(self):
        id1 = EntityId.create()
        id2 = EntityId.create()
        assert id1 != id2

    def test_of_parses_valid_uuid(self):
        id1 = EntityId.create()
        id2 = EntityId.of(str(id1))
        assert id1 == id2

    def test_of_raises_on_invalid_uuid(self):
        with pytest.raises(ValueError):
            EntityId.of("not-a-uuid")

    def test_equality(self):
        id1 = EntityId.create()
        id2 = EntityId(id1.uuid)
        assert id1 == id2
        assert hash(id1) == hash(id2)

    def test_inequality_with_other_type(self):
        id1 = EntityId.create()
        assert id1 != "not-an-entity-id"


class TestMember:
    def test_create_member_with_valid_data(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        assert member.email == "test@example.com"
        assert member.name == "Test User"
        assert member.deleted is False

    def test_passwd_is_hashed(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        assert member.passwd != VALID_PASSWORD
        assert member.passwd.startswith("$2b$")

    def test_verify_passwd(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        assert member.verify_passwd(VALID_PASSWORD) is True
        assert member.verify_passwd("WrongPassword@1") is False

    def test_update_profile(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Old Name")
        member.update_profile(name="New Name")
        assert member.name == "New Name"

    def test_update_profile_with_none_keeps_name(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Old Name")
        member.update_profile(name=None)
        assert member.name == "Old Name"

    def test_change_email(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        member.change_email("new@example.com")
        assert member.email == "new@example.com"

    def test_change_email_none_raises(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        with pytest.raises((TypeError, ValueError)):
            member.change_email(None)

    def test_change_passwd(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        new_passwd = "NewPass@123"
        member.change_passwd(new_passwd)
        assert member.verify_passwd(new_passwd) is True
        assert member.verify_passwd(VALID_PASSWORD) is False

    def test_change_passwd_none_raises(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        with pytest.raises((TypeError, ValueError)):
            member.change_passwd(None)

    def test_delete(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test User")
        member.delete()
        assert member.deleted is True

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError, match="valid email"):
            Member(email="not-an-email", passwd=VALID_PASSWORD, name="Test")

    def test_short_passwd_raises(self):
        with pytest.raises(ValueError, match="at least 8"):
            Member(email="test@example.com", passwd="Ab@1", name="Test")

    def test_passwd_without_special_char_raises(self):
        with pytest.raises(ValueError, match="special character"):
            Member(email="test@example.com", passwd="Abcdefgh1", name="Test")

    def test_passwd_without_lowercase_raises(self):
        with pytest.raises(ValueError, match="lowercase"):
            Member(email="test@example.com", passwd="ABCDEFG@1", name="Test")

    def test_passwd_without_uppercase_raises(self):
        with pytest.raises(ValueError, match="uppercase"):
            Member(email="test@example.com", passwd="abcdefg@1", name="Test")
