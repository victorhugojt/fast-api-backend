import os
from fastapi import FastAPI
from app.controllers import basic_controller, greetings_controller, coins_controller, decorated_controller
from app.instrumentation import traces_exporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(title='fastAPI self training', version = '1.0.0', root_path = '')

tracer = traces_exporter.config('greeting-service', os.environ.get("MODE", "otlp-grpc"))

FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)

app.include_router(greetings_controller.router)
app.include_router(coins_controller.router)
app.include_router(basic_controller.router)
app.include_router(decorated_controller.router)
