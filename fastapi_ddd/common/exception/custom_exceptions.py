from typing import Optional

from fastapi import status


class BaseAppException(Exception):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    ERROR_MESSAGE = "Bad request error occurred"

    def __init__(
        self,
        message: str = ERROR_MESSAGE,
        origin_exception: Optional[Exception] = None,
        error_code: int = STATUS_CODE,
    ) -> None:
        self.message = message
        self.origin_exception = origin_exception or Exception(message)
        self.error_code = error_code


class DatabaseException(BaseAppException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    ERROR_MESSAGE = "A database exception occurred."

    def __init__(
        self,
        message: str = ERROR_MESSAGE,
        origin_exception: Optional[Exception] = None,
        error_code: int = STATUS_CODE,
    ) -> None:
        self.message = message
        self.origin_exception = origin_exception if origin_exception else Exception(message)
        self.error_code = error_code


class DatabaseIdNotFoundException(DatabaseException):
    ERROR_MESSAGE = "ID does not exist."

    def __init__(
        self,
        message: str = ERROR_MESSAGE,
        origin_exception: Optional[Exception] = None,
        error_code: int = DatabaseException.STATUS_CODE,
    ) -> None:
        super().__init__(message, origin_exception, error_code)
