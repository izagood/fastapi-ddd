from fastapi import Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi_ddd.common.exception.custom_exceptions import (
    BaseAppException,
    DatabaseException,
)

HTTP_500_INTERNAL_SERVER_ERROR_MESSAGE: str = "Unknown server error"
HTTP_400_BAD_REQUEST_MESSAGE: str = "Bad request error occurred"


async def internal_server_exception_handler(
    request: Request,
    exc: Exception,
) -> ORJSONResponse:
    logger.error("Internal server error")
    logger.exception(exc)
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=HTTP_500_INTERNAL_SERVER_ERROR_MESSAGE,
    )


async def base_app_exception_handler(
    request: Request,
    exc: BaseAppException,
) -> ORJSONResponse:
    logger.error(f"error messages : {exc.message}")
    logger.exception(exc)
    return ORJSONResponse(
        status_code=exc.error_code,
        content=exc.message,
    )


async def database_exception_handler(
    request: Request,
    exc: DatabaseException,
) -> ORJSONResponse:
    logger.error(f"error messages : {exc.message}")
    logger.exception(exc)
    return ORJSONResponse(
        status_code=exc.error_code,
        content=exc.message,
    )


async def custom_http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    logger.error(f"error messages : {exc.detail}")
    return await http_exception_handler(request, exc)


exception_handlers = {
    DatabaseException: database_exception_handler,
    StarletteHTTPException: custom_http_exception_handler,
    BaseAppException: base_app_exception_handler,
    Exception: internal_server_exception_handler,
}
