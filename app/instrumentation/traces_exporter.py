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


OTLP_GRPC_ENDPOINT = os.environ.get('OTLP_TRACES_GRPC_ENDPOINT')
OTLP_HTTP_ENDPOINT = os.environ.get('OTLP_TRACES_HTTP_ENDPOINT')


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
        tracer.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporterGRPC(endpoint=OTLP_GRPC_ENDPOINT, insecure=True)
            )
        )

    return tracer

    