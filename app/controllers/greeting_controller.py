from fastapi import APIRouter, HTTPException, Response
import os
import random
import prometheus_client
from opentelemetry import trace, baggage
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.context import attach, detach

from app.span_utils import custom_processor

# provider = TracerProvider()
# processor = BatchSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(processor)
provider = TracerProvider(resource=Resource.create({"service.name": "greetings-service"}))
processor = custom_processor.MySpanProcessor(span_exporter=ConsoleSpanExporter())
provider.add_span_processor(span_processor=processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


router = APIRouter()

heads_count = prometheus_client.Counter(
    "heads_count", "Number of heads"
)

tails_count = prometheus_client.Counter(
    "tails_count", "Number of tails"
)

flip_count = prometheus_client.Counter(
    "flip_count", "Number of flips"
)

@router.get("/", status_code=200)
async def info():
    return {"message": "Ready"}


@router.get("/ping", status_code=200)
async def info():
    return {"pong !"}


def another_thing_to_do():
    return "have a good weekend"


@router.get("/hi", status_code=200)
async def greeting():
    user = attach(
        baggage.set_baggage("user.id", "Pibe Valderrama")
    )
    with tracer.start_as_current_span("Greeting Request", attributes={ "requires env": "HOME", "library":"FastAPI" } ):
        parent_context = baggage.set_baggage("position", "10")
        name = os.environ['NAME']
        with tracer.start_as_current_span("Child Span", context=parent_context):
            child_context = baggage.set_baggage("matches", "467")
            message = "Hello {} !. {}".format(name, another_thing_to_do())
            print("-------------------------------------------------------")
            print(baggage.get_baggage("user.id", parent_context))
            print(baggage.get_baggage("position", parent_context))
            print("-------------------------------------------------------")
            print(baggage.get_baggage("matches", child_context))
            print(baggage.get_baggage("user.id", child_context))
            print("-------------------------------------------------------")

            detach(user)

            return {"message": message}
    
    


@router.get("/flip-coins", status_code=200)
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Times must be set in request and should be an Integer"
        )
    
    times_int = int(times)

    heads = 0
    for _ in range(times_int):
        if random.randint(0,1):
            heads += 1
    tails = times_int - heads

    heads_count.inc(heads)
    tails_count.inc(tails)
    flip_count.inc(times_int)

    return {
        "heads": heads,
        "tails": tails,
    }

@router.get("/metrics", status_code=200)
def get_metrics():
    return Response( content=prometheus_client.generate_latest(), media_type="text/plain")


