from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def info():
    return {"message": "Ready"}


@router.get("/ping")
async def info():
    return {"pong !"}


@router.get("/hi")
async def greeting():
    return {"message": "Hello Champion !!!"}