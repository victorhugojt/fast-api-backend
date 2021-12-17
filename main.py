from fastapi import FastAPI
from api.v1.app import api_router

app = FastAPI()

app.include_router(api_router)
