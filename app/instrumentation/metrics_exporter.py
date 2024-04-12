import os
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


OTLP_HTTP_ENDPOINT = os.environ.get('OTLP_METRICS_HTTP_ENDPOINT')


def set_resource(service_name):
    return Resource(attributes={SERVICE_NAME: service_name})


def config(service_name) -> None:
    metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=OTLP_HTTP_ENDPOINT)
)
    meter_provider = MeterProvider(resource=set_resource(service_name), metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    return metrics