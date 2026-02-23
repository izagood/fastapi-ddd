from fastapi_ddd.domain.member.member_validator import EmailValidator, PasswordHasher, PasswordValidator


class Email:
    def __init__(self, value: str) -> None:
        self._value = EmailValidator.validate(value)

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Email({self._value!r})"


class Password:
    def __init__(self, plain: str) -> None:
        PasswordValidator.validate(plain)
        self._hashed = PasswordHasher.hash(plain)

    @classmethod
    def from_hashed(cls, hashed: str) -> "Password":
        instance = object.__new__(cls)
        instance._hashed = hashed
        return instance

    @property
    def hashed_value(self) -> str:
        return self._hashed

    def verify(self, plain: str) -> bool:
        return PasswordHasher.verify(plain, self._hashed)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Password):
            return self._hashed == other._hashed
        return False

    def __hash__(self) -> int:
        return hash(self._hashed)

    def __repr__(self) -> str:
        return "Password(***)"
