from fastapi import APIRouter

router = APIRouter()

@router.get("/hi")
async def greeting():
    return {"message": "Hello World"}