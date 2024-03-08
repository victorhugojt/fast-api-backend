from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace, baggage
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.context import attach, detach
from fastapi import APIRouter, HTTPException
import os
import random
import time

router = APIRouter()


# Setting global service name for exporter
resource = Resource(attributes={
    SERVICE_NAME: "greeting-service"
})

# Traces Exporter Setup
trace_provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4318/v1/traces"))
trace_provider.add_span_processor(processor)
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)


# Metrics Exporter Setup
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://collector:4318/v1/metrics")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)
http_requests_counter = meter.create_counter("http_requests_counter")
heads_count = meter.create_counter("heads_count")
tails_count = meter.create_counter("tails_count")
flip_count  = meter.create_counter("flip_count")
http_rt = meter.create_histogram("histogram")



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
           
            detach(user)

            return {"message": message}


def message():
    return "have a good weekend"


@router.get("/goodbye", status_code=200)
async def goodbye():
    
    start_time = time.perf_counter()
    user_name = os.environ['NAME']
    
    user = attach(
        baggage.set_baggage("user.name", user_name)
    )
    with tracer.start_as_current_span("Greeting Request", attributes={ "Requires environment var": "NAME", "library":"FastAPI" } ):
        parent_context = baggage.set_baggage("user.id", "10002494")
        
        with tracer.start_as_current_span("Child Span", context=parent_context):
            child_context = baggage.set_baggage("role", "Performance Engineer")
            message = "Goodbye {} !. {}".format(user_name, message())

            detach(user)
            
            http_requests_counter.add(1)

            response_time = time.perf_counter() - start_time
            http_rt.record(response_time)

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

    heads_count.add(heads)
    tails_count.add(tails)
    flip_count.add(times_int)

    return {
        "heads": heads,
        "tails": tails,
    }