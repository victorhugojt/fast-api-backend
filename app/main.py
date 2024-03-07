from fastapi import FastAPI
from app.controllers import instrumentalized_controller, simple_controller

app = FastAPI(title='fastAPI self training', version = '1.0.0', root_path = '')

app.include_router(instrumentalized_controller.router)

app.include_router(simple_controller.router)
