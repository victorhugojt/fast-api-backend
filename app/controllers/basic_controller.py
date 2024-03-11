from fastapi import APIRouter

router = APIRouter()


@router.get("/basic")
async def info():
    return {"chao !"}
