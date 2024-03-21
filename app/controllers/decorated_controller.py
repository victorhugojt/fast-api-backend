from fastapi import APIRouter
from opentelemetry import trace
from app.instrumentation.instrument import span

router = APIRouter()
tracer = trace.get_tracer(__name__)


@router.get("/thanks")
@span(tracer, "Greeting Request", { "Requires environment var": "NAME", "library":"FastAPI", "pattern":"decorated" })
def info():
    return 'You are welcome !!!!!!! '
