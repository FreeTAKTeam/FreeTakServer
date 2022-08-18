import socket
from typing import Dict, Tuple
from FreeTAKServer.controllers.SendDataController import SendDataController
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.routing.controller import Controller
from digitalpy.core.object_factory import ObjectFactory

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
    
    # TODO: the issue is we need to deal with different formats of messages being sent to users,
    # I see a number of different ways this can be implemented at a high level
    # 1. add the logic to the orchestrator, basically call the serializer before calling broadcast and send the message strings
    # 2. add the logic to the orchestrator, basically call a separate sender component per message format (xml, protobuf etc...)
    # 3. add the logic to the broadcast layer, basically call the broadcast layer which will then determine the client type and pass it off to the respective component
    # 4. add the logic to the client layer, basically abstract the send method so the client object will serialize the message itself before being sent
    # 5. add the parser as part of the message context?
    # temporarily decided on a form of dependencie injection where the parsing action is passed as a parameter and then called
    def broadcast(self, model_objects: list, clients: Dict[str, Tuple[socket.socket, ClientInformation]], sender: ClientInformation, model_object_parser: str, **kwargs):
        self.response.set_values(kwargs)
        
        request = ObjectFactory.get_new_instance('request')
        request.set_action(model_object_parser)
        request.set_value("model_objects", model_objects)
        actionmapper = ObjectFactory.get_instance('actionMapper')
        response = ObjectFactory.get_new_instance('response')
        actionmapper.process_action(request, response)
        
        for message in response.get_value('messages'):
            for uid, client in clients.items():
                client[0].send(message)
