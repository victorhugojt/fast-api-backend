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

from fastapi import APIRouter
import os
import time

router = APIRouter()


# Setting global service name for exporter
resource = Resource(attributes={
    SERVICE_NAME: "greeting-service"
})

# Traces Exporter Setup
trace_provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="collector:4318/v1/traces"))
trace_provider.add_span_processor(processor)
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)

# Metrics Exporter Setup
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="collector:4318/v1/metrics")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)
http_requests_counter = meter.create_counter("http_requests_counter")
http_rt = meter.create_histogram("histogram")


def message():
    return "have a good weekend"


router.get("/goodbye", status_code=200)
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
            print("-------------------------------------------------------")
            print(baggage.get_baggage("user.name", parent_context))
            print(baggage.get_baggage("role", parent_context))
            print("-------------------------------------------------------")
            print(baggage.get_baggage("role", child_context))
            print(baggage.get_baggage("user.id", child_context))
            print("-------------------------------------------------------")

            detach(user)
            
            http_requests_counter.add(1)

            response_time = time.perf_counter() - start_time
            http_rt.record(response_time)

            return {"message": message}
