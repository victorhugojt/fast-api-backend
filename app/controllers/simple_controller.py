from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/goodbye")
async def info():
    return {"chao !"}
