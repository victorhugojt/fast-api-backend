import os
from fastapi import FastAPI
from app.controllers import basic_controller, greetings_controller, coins_controller
from app.instrumentation import traces
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(title='fastAPI self training', version = '1.0.0', root_path = '')

tracer = traces.config('greeting-service', os.environ.get("MODE", "otlp-grpc"))

FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)

app.include_router(greetings_controller.router)
app.include_router(coins_controller.router)
app.include_router(basic_controller.router)
