import pytest

from fastapi_ddd.domain.member.member_validator import EmailValidator, PasswordHasher, PasswordValidator


class TestEmailValidator:
    def test_valid_email(self):
        result = EmailValidator.validate("user@example.com")
        assert result == "user@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValueError, match="valid email"):
            EmailValidator.validate("not-an-email")

    def test_empty_email(self):
        with pytest.raises(ValueError):
            EmailValidator.validate("")


class TestPasswordValidator:
    def test_valid_password(self):
        result = PasswordValidator.validate("Test@1234")
        assert result == "Test@1234"

    def test_short_password(self):
        with pytest.raises(ValueError, match="at least 8"):
            PasswordValidator.validate("Ab@1")

    def test_no_special_character(self):
        with pytest.raises(ValueError, match="special character"):
            PasswordValidator.validate("Abcdefgh1")

    def test_no_lowercase(self):
        with pytest.raises(ValueError, match="lowercase"):
            PasswordValidator.validate("ABCDEFG@1")

    def test_no_uppercase(self):
        with pytest.raises(ValueError, match="uppercase"):
            PasswordValidator.validate("abcdefg@1")

    def test_validate_and_hash_returns_hashed(self):
        result = PasswordValidator.validate_and_hash("Test@1234")
        assert result != "Test@1234"
        assert result.startswith("$2b$")


class TestPasswordHasher:
    def test_hash_produces_bcrypt_hash(self):
        hashed = PasswordHasher.hash("Test@1234")
        assert hashed.startswith("$2b$")

    def test_hash_is_not_plaintext(self):
        hashed = PasswordHasher.hash("Test@1234")
        assert hashed != "Test@1234"

    def test_verify_correct_password(self):
        hashed = PasswordHasher.hash("Test@1234")
        assert PasswordHasher.verify("Test@1234", hashed) is True

    def test_verify_wrong_password(self):
        hashed = PasswordHasher.hash("Test@1234")
        assert PasswordHasher.verify("Wrong@1234", hashed) is False

    def test_different_hashes_for_same_password(self):
        hash1 = PasswordHasher.hash("Test@1234")
        hash2 = PasswordHasher.hash("Test@1234")
        assert hash1 != hash2  # bcrypt uses random salt
