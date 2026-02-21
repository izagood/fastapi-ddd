import re

import bcrypt
from email_validator import EmailNotValidError, validate_email


class EmailValidator:
    @staticmethod
    def validate(email: str) -> str:
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError("value is not a valid email address")
        return email


class PasswordValidator:
    @staticmethod
    def validate(passwd: str) -> str:
        PasswordValidator._validate_min_passwd_length(passwd)
        PasswordValidator._validate_special_character(passwd)
        PasswordValidator._validate_lowercase_letter(passwd)
        PasswordValidator._validate_uppercase_letter(passwd)

        return passwd

    @staticmethod
    def validate_and_hash(passwd: str) -> str:
        PasswordValidator.validate(passwd)
        return PasswordHasher.hash(passwd)

    @staticmethod
    def _validate_min_passwd_length(passwd):
        min_passwd_length = 8
        if len(passwd) < min_passwd_length:
            raise ValueError(f"passwd must be at least {min_passwd_length} characters")

    @staticmethod
    def _validate_special_character(passwd):
        special_chars = r'[!@#$%^&*()_+\-=\[\]{};\\:"|,.<>\/?]'
        if not re.search(special_chars, passwd):
            raise ValueError("Your password must contain at least one special character.")

    @staticmethod
    def _validate_lowercase_letter(passwd):
        if not any(char.islower() for char in passwd):
            raise ValueError("Your password must contain at least one lowercase letter.")

    @staticmethod
    def _validate_uppercase_letter(passwd):
        if not any(char.isupper() for char in passwd):
            raise ValueError("Your password must contain at least one uppercase letter.")


class PasswordHasher:
    @staticmethod
    def hash(passwd: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(passwd.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify(passwd: str, hashed: str) -> bool:
        return bcrypt.checkpw(passwd.encode("utf-8"), hashed.encode("utf-8"))
