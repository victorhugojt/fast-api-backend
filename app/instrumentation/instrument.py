from functools import wraps


def span(tracer, span_name: str = "", attributes = None):

    def span_decorator(func):

        def _set_attributes(span, attributes_dict):
            if attributes_dict:
                for att in attributes_dict:
                    span.set_attribute(att, attributes_dict[att])

        @wraps(func)
        async def wrap_with_span(*args, **kwargs):
            with tracer.start_as_current_span(span_name, attributes) as span:
                _set_attributes(span, attributes)
                return func(*args, **kwargs)

        return wrap_with_span

    return span_decorator
