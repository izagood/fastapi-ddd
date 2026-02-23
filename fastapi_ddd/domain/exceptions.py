class DomainException(Exception):
    def __init__(self, message: str = "Domain rule violation") -> None:
        self.message = message
        super().__init__(message)


class EntityNotFoundException(DomainException):
    def __init__(self, message: str = "Entity not found") -> None:
        super().__init__(message)


class MemberNotFoundException(EntityNotFoundException):
    def __init__(self, message: str = "Member not found") -> None:
        super().__init__(message)


class DuplicateEmailException(DomainException):
    def __init__(self, email: str = "") -> None:
        message = f"Email already exists: {email}" if email else "Email already exists"
        super().__init__(message)
