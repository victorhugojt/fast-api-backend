from fastapi import FastAPI
from app.controllers import complex_controller# instrumentalized_controller, simple_controller

app = FastAPI(title='fastAPI self training', version = '1.0.0', root_path = '')

app.include_router(complex_controller.router)
