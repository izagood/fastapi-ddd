from fastapi_ddd.domain.events import MemberCreated, MemberDeleted, MemberEmailChanged
from fastapi_ddd.domain.member.member import Member

VALID_PASSWORD = "Test@1234"


class TestDomainEvents:
    def test_member_created_event_on_init(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test")
        events = member.domain_events
        assert len(events) == 1
        assert isinstance(events[0], MemberCreated)
        assert events[0].email == "test@example.com"

    def test_member_email_changed_event(self):
        member = Member(email="old@example.com", passwd=VALID_PASSWORD, name="Test")
        member.clear_events()
        member.change_email("new@example.com")
        events = member.domain_events
        assert len(events) == 1
        assert isinstance(events[0], MemberEmailChanged)
        assert events[0].old_email == "old@example.com"
        assert events[0].new_email == "new@example.com"

    def test_member_deleted_event(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test")
        member.clear_events()
        member.delete()
        events = member.domain_events
        assert len(events) == 1
        assert isinstance(events[0], MemberDeleted)

    def test_clear_events(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test")
        assert len(member.domain_events) == 1
        member.clear_events()
        assert len(member.domain_events) == 0

    def test_domain_events_returns_copy(self):
        member = Member(email="test@example.com", passwd=VALID_PASSWORD, name="Test")
        events = member.domain_events
        events.clear()
        assert len(member.domain_events) == 1
