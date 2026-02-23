from fastapi import APIRouter

from fastapi_ddd.presentation.rest import member_router

api_router: APIRouter = APIRouter()
api_router.include_router(router=member_router.router, prefix="/members", tags=["Member"])


@api_router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
