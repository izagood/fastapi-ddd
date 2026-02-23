from typing import Optional

from fastapi import status


class BaseAppException(Exception):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    ERROR_MESSAGE = "An unexpected error occurred"

    def __init__(
        self,
        message: str = ERROR_MESSAGE,
        origin_exception: Optional[Exception] = None,
        error_code: int = STATUS_CODE,
    ) -> None:
        self.message = message
        self.origin_exception = origin_exception or Exception(message)
        self.error_code = error_code


class NotFoundException(BaseAppException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    ERROR_MESSAGE = "Resource not found"

    def __init__(
        self,
        message: str = ERROR_MESSAGE,
        origin_exception: Optional[Exception] = None,
        error_code: int = STATUS_CODE,
    ) -> None:
        super().__init__(message, origin_exception, error_code)


class DatabaseException(BaseAppException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    ERROR_MESSAGE = "A database exception occurred."

    def __init__(
        self,
        message: str = ERROR_MESSAGE,
        origin_exception: Optional[Exception] = None,
        error_code: int = STATUS_CODE,
    ) -> None:
        super().__init__(message, origin_exception, error_code)
