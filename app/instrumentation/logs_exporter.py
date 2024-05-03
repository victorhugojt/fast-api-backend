import os
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


OTLP_HTTP_ENDPOINT = os.environ.get('OTLP_LOGS_HTTP_ENDPOINT')

def set_resource(service_name):
    return Resource.create(
                {
                "service.name": service_name,
                "service.instance.id": "local",
                }
            )


def config(service_name):
    logger_provider = LoggerProvider(set_resource(service_name))
    set_logger_provider(logger_provider)
    otlp_exporter = OTLPLogExporter(endpoint=OTLP_HTTP_ENDPOINT, insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

    return logger_provider


def set_handler(level, logger_provider):
    return LoggingHandler(level, logger_provider)
    

