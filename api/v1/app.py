from fastapi import APIRouter
from api.v1.controllers import greeting_controller

api_router = APIRouter()

api_router.include_router(greeting_controller.router, prefix='/greetings')