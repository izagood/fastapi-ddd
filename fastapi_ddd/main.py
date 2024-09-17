from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from loguru import logger

from fastapi_ddd.common.config.app_config import app_settings
from fastapi_ddd.common.config.logger import init_logging
from fastapi_ddd.common.exception.exception_handlers import exception_handlers
from fastapi_ddd.presentation.rest.routers import api_router

init_logging()

app = FastAPI(
    title=app_settings.FAST_API.TITLE,
    version=app_settings.FAST_API.VERSION,
    exception_handlers=exception_handlers,
    default_response_class=ORJSONResponse,
)
app.include_router(router=api_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request {request.method} {request.url}")

    body = await request.body()
    request.state.body = body

    logger.info(f"Request Body: {body.decode('utf-8')}")

    response = await call_next(request)

    logger.info(f"Response status code: {response.status_code}")

    return response


origins = ["*"]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Run FastAPI DDD backend Example")
