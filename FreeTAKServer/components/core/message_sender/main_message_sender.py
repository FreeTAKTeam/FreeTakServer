import socket
from typing import Dict, Tuple
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory

from FreeTAKServer.model.ClientInformation import ClientInformation


class MessageSender(Controller):
    def __init__(self):
        pass

    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def broadcast(
        self,
        model_objects: list,
        clients: Dict[str, Tuple[socket.socket, ClientInformation]],
        sender: ClientInformation,
        model_object_parser: str,
        **kwargs
    ):
        self.response.set_values(kwargs)

        request = ObjectFactory.get_new_instance("request")
        request.set_action(model_object_parser)
        request.set_value("model_objects", model_objects)
        actionmapper = ObjectFactory.get_instance("actionMapper")
        response = ObjectFactory.get_new_instance("response")
        actionmapper.process_action(request, response)

        for message in response.get_value("messages"):
            for uid, client in clients.items():
                client[0].send(message)
