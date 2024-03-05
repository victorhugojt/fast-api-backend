from fastapi import FastAPI
from app.controllers import greeting_controller, simple_controller, good_bye_controller

app = FastAPI(title='fastAPI self training', version = '1.0.0', root_path = '')

app.include_router(good_bye_controller.router)

app.include_router(greeting_controller.router)

app.include_router(simple_controller.router)
