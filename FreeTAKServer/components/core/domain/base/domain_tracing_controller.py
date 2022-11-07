from digitalpy.component.impl.default_tracing_controller import TracingController
from ..configuration.domain_constants import COMPONENT_NAME
from opentelemetry.trace import Status, StatusCode


class DomainTracingController(TracingController):
    """this controller is responsible for instantiating and handling tracing activities"""

    def __init__(self, request, response, action_mapper, configuration):
        super().__init__(
            COMPONENT_NAME, request, response, action_mapper, configuration
        )

    def test_tracing(self):
        """test the tracing functionality of the domain tracing controller"""
        with self.tracer.start_as_current_span("test_span") as span:
            print("testing 1+1")
            print(1 + 1)
            span.add_event("completed")
            try:
                raise Exception("some exception")
            except Exception as ex:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(ex)
