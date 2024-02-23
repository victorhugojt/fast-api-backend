from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import SpanKind


class MySpanProcessor(BatchSpanProcessor):
    def on_end(self, span: ReadableSpan) -> None:
        if span.kind == SpanKind.INTERNAL and (
                span.attributes.get('type', None) in ('http.request',
                                                      'http.response.start',
                                                      'http.response.body')
        ):
            return
        super().on_end(span=span)