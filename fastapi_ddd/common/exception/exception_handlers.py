from fastapi import Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi_ddd.common.exception.custom_exceptions import (
    BaseAppException,
    DatabaseException,
    NotFoundException,
)
from fastapi_ddd.domain.exceptions import (
    DomainException,
    DuplicateEmailException,
    EntityNotFoundException,
)


async def internal_server_exception_handler(
    request: Request,
    exc: Exception,
) -> ORJSONResponse:
    logger.error("Internal server error")
    logger.exception(exc)
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Unknown server error"},
    )


async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException,
) -> ORJSONResponse:
    logger.warning(f"Not found: {exc.message}")
    return ORJSONResponse(
        status_code=exc.error_code,
        content={"error": exc.message},
    )


async def base_app_exception_handler(
    request: Request,
    exc: BaseAppException,
) -> ORJSONResponse:
    logger.error(f"Application error: {exc.message}")
    logger.exception(exc)
    return ORJSONResponse(
        status_code=exc.error_code,
        content={"error": exc.message},
    )


async def database_exception_handler(
    request: Request,
    exc: DatabaseException,
) -> ORJSONResponse:
    logger.error(f"Database error: {exc.message}")
    logger.exception(exc)
    return ORJSONResponse(
        status_code=exc.error_code,
        content={"error": exc.message},
    )


async def custom_http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    logger.error(f"HTTP error: {exc.detail}")
    return await http_exception_handler(request, exc)


async def domain_entity_not_found_handler(
    request: Request,
    exc: EntityNotFoundException,
) -> ORJSONResponse:
    logger.warning(f"Entity not found: {exc.message}")
    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exc.message},
    )


async def duplicate_email_handler(
    request: Request,
    exc: DuplicateEmailException,
) -> ORJSONResponse:
    logger.warning(f"Duplicate email: {exc.message}")
    return ORJSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": exc.message},
    )


async def domain_exception_handler(
    request: Request,
    exc: DomainException,
) -> ORJSONResponse:
    logger.warning(f"Domain error: {exc.message}")
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": exc.message},
    )


async def value_error_handler(
    request: Request,
    exc: ValueError,
) -> ORJSONResponse:
    logger.warning(f"Bad request: {exc}")
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": str(exc)},
    )


exception_handlers = {
    DuplicateEmailException: duplicate_email_handler,
    EntityNotFoundException: domain_entity_not_found_handler,
    DomainException: domain_exception_handler,
    ValueError: value_error_handler,
    NotFoundException: not_found_exception_handler,
    DatabaseException: database_exception_handler,
    StarletteHTTPException: custom_http_exception_handler,
    BaseAppException: base_app_exception_handler,
    Exception: internal_server_exception_handler,
}
