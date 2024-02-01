from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/", status_code=200)
async def info():
    return {"message": "Ready"}


@router.get("/ping", status_code=200)
async def info():
    return {"pong !"}


@router.get("/hi", status_code=200)
async def greeting():
    name = os.environ['NAME']
    return {"message": "Hello {} !".format(name)}