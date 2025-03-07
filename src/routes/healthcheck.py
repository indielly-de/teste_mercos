from fastapi import APIRouter

healthcheck_router = APIRouter(prefix="/healthcheck")


@healthcheck_router.get("/")
async def healthcheck():
    return {"status": "ok"}
