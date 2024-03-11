import os
from fastapi import FastAPI
from app.controllers import refactor_controller
from app.instrumentation import traces
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(title='fastAPI self training', version = '1.0.0', root_path = '')

tracer = traces.config('greeting-service', os.environ.get("MODE", "otlp-grpc"))

FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)

app.include_router(refactor_controller.router)
