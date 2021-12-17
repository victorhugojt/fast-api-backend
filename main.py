from fastapi import FastAPI
from api.v1.app import api_router

app = FastAPI(title='fastAPI self training', version = '1.0.0', root_path = '')

app.include_router(api_router)
