import pytest

from fastapi_ddd.domain.member.value_objects import Email, Password

VALID_PASSWORD = "Test@1234"


class TestEmail:
    def test_create_valid_email(self):
        email = Email("user@example.com")
        assert email.value == "user@example.com"
        assert str(email) == "user@example.com"

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError, match="valid email"):
            Email("not-an-email")

    def test_equality(self):
        e1 = Email("a@example.com")
        e2 = Email("a@example.com")
        assert e1 == e2
        assert hash(e1) == hash(e2)

    def test_inequality(self):
        e1 = Email("a@example.com")
        e2 = Email("b@example.com")
        assert e1 != e2

    def test_inequality_with_other_type(self):
        e = Email("a@example.com")
        assert e != "a@example.com"


class TestPassword:
    def test_create_valid_password(self):
        pw = Password(VALID_PASSWORD)
        assert pw.hashed_value.startswith("$2b$")

    def test_weak_password_raises(self):
        with pytest.raises(ValueError, match="at least 8"):
            Password("Ab@1")

    def test_verify_correct(self):
        pw = Password(VALID_PASSWORD)
        assert pw.verify(VALID_PASSWORD) is True

    def test_verify_wrong(self):
        pw = Password(VALID_PASSWORD)
        assert pw.verify("Wrong@1234") is False

    def test_from_hashed(self):
        pw = Password(VALID_PASSWORD)
        restored = Password.from_hashed(pw.hashed_value)
        assert restored.verify(VALID_PASSWORD) is True

    def test_repr_hides_value(self):
        pw = Password(VALID_PASSWORD)
        assert "***" in repr(pw)
        assert VALID_PASSWORD not in repr(pw)
