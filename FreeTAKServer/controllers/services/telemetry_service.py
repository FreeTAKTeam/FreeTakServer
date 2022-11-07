import zmq
import json


class TelemetryService:
    def __init__(self):
        self.telemetry_data = []

    def instantiate_sockets(self, host="127.0.0.1", port=40033):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.bind(f"tcp://{host}:{port}")
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")

    def main(self):
        self.instantiate_sockets()
        while True:
            try:
                self.telemetry_data.append(
                    json.loads(self.socket.recv_multipart()[0].decode())
                )
                print(self.telemetry_data)
            except Exception as e:
                print(e)
