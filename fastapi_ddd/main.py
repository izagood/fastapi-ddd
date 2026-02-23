from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from loguru import logger

from fastapi_ddd.common.config.app_config import app_settings
from fastapi_ddd.common.config.logger import init_logging
from fastapi_ddd.common.exception.exception_handlers import exception_handlers
from fastapi_ddd.infra.database.init_db import close_db, init_db
from fastapi_ddd.presentation.rest.routers import api_router

init_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=app_settings.FAST_API.TITLE,
    version=app_settings.FAST_API.VERSION,
    exception_handlers=exception_handlers,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
app.include_router(router=api_router, prefix="/api/v1")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response {request.method} {request.url} - {response.status_code}")
    return response


cors = app_settings.CORS
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=cors.origins_list,
    allow_credentials=cors.CORS_ALLOW_CREDENTIALS,
    allow_methods=cors.methods_list,
    allow_headers=cors.headers_list,
)

logger.info("Run FastAPI DDD backend Example")
