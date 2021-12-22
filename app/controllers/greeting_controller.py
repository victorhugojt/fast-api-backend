from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/")
async def info():
    return {"message": "Ready"}


@router.get("/ping")
async def info():
    return {"pong !"}


@router.get("/hi")
async def greeting():
    name = os.environ['NAME']
    return {"message": "Hello {} !".format(name)}