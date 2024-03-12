import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterGRPC,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterHTTP,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


OTLP_GRPC_ENDPOINT = "collector:4317"
OTLP_HTTP_ENDPOINT = "http://collector:4318/v1/traces"


def set_resource(service_name):
    return Resource(attributes={SERVICE_NAME: service_name})

def config(service_name, mode) -> None:
    tracer = TracerProvider(resource=set_resource(service_name))
    trace.set_tracer_provider(tracer)

    if mode == "otlp-grpc":
        tracer.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporterGRPC(endpoint=OTLP_GRPC_ENDPOINT, insecure=True)
            )
        )
    elif mode == "otlp-http":
        tracer.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporterHTTP(endpoint=OTLP_HTTP_ENDPOINT))
        )
    else:
        # default otlp-grpc
        tracer.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporterGRPC(endpoint=OTLP_GRPC_ENDPOINT, insecure=True)
            )
        )

    return tracer

    