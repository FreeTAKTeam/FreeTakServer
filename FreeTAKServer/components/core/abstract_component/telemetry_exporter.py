from opentelemetry.sdk.trace.export import SpanExporter
import zmq
from typing import Optional, Sequence
from opentelemetry.sdk.trace import ReadableSpan, Span, SpanProcessor
import json


class ZMQExporter(SpanExporter):
    def __init__(self, port: int, host: str):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect(f"tcp://{host}:{port}")

    def export(self, spans: Sequence[ReadableSpan]):
        for span in spans:
            try:
                self.socket.send_string(span.to_json())
            except Exception as e:
                print(e)

    def shutdown(self) -> None:
        self.socket.close()

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        # pylint: disable=unused-argument
        return True
