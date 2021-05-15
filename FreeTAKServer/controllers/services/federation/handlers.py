from abc import ABC
from FreeTAKServer.controllers.services.service_abstracts import ServerServiceInterface, ServiceInterface
from FreeTAKServer.model.federate import Federate
from FreeTAKServer.model.clients import ClientAbstract
from FreeTAKServer.controllers.configuration.Types import Types
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.SpecificCoT.SpecificCoTAbstract import SpecificCoTAbstract
from FreeTAKServer.controllers.SpecificCoTControllers.SendCoTAbstractController import SendCoTAbstractController

class HandlerInterface(ABC):
    
    def Handle(self, obj, command):
        raise NotImplementedError

    def setNextHandler(self, handler):
        raise NotImplementedError

class HandlerBase(HandlerInterface):
    """ implements basic functionality required for all handlers

    this class implements the setNextHandler method from the HandlerInterface
    as well as creating a callNextHandler method which will either call the next
    handler in the chain of responsibility or raise an exception if there are no
    remaining handlers.
    """

    def __init__(self):
        self.nextHandler = None

    def Handle(self, obj: ServiceInterface, command):
        raise NotImplementedError
    
    def setNextHandler(self, handler: HandlerInterface):
        """ set next handler to be called in chain of responsibility

        :params handler: the handler which should be next in chain of responsibility
        """

        self.nextHandler = handler

    def callNextHandler(self, obj: ServiceInterface, command):
        if self.nextHandler is None:
            raise Exception("no further handlers, object not supported by responsibility chain")
        else:
            self.nextHandler.Handle(obj, command)

class ConnectHandler(HandlerBase):
    """ Handler for command to connect to new server

    """
    def Handle(self, obj: ServiceInterface, command):
        if isinstance(command, tuple) and command[1] == "CREATE":
            obj.connect_to_server(command)

        else:
            self.callNextHandler(obj, command)

class DisconnectHandler(HandlerBase):
    """ Handler for command to disconnect client

    """

    def Handle(self, obj: ServiceInterface, command):
        if isinstance(obj, ServerServiceInterface) and isinstance(command, tuple) and command[1] == "DELETE":
            obj.disconnect_client(command[0])

        else:
            self.callNextHandler(obj, command)

class SendDataHandler(HandlerBase):
    """ Handler for command send data to client

    """

    def Handle(self, obj: ServiceInterface, command: any):

        if isinstance(obj, ServerServiceInterface) and isinstance(command, SpecificCoTAbstract):
            obj.send_data_to_clients(command)

        else:
            self.callNextHandler(obj, command)

class SendConnectionDataHandler(HandlerBase):

    def Handle(self, obj: ServiceInterface, command: any):
        from FreeTAKServer.model.ClientInformation import ClientInformation

        if isinstance(obj, ServerServiceInterface) and isinstance(command, ClientInformation):
            obj.send_connection_data(command)
            return None
        else:
            self.callNextHandler(obj, command)

class SendDisconnectionDataHandler(HandlerBase):
    def Handle(self, obj: ServiceInterface, command):
        from FreeTAKServer.model.SpecificCoT.SendDisconnect import SendDisconnect

        if isinstance(obj, ServerServiceInterface) and isinstance(command, SendDisconnect):
            obj.send_disconnection_data(command)

        else:
            self.callNextHandler(obj, command)

class StopHandler(HandlerBase):
    """ Handler for command stop service

    """

    def Handle(self, obj: ServiceInterface, command):

        if isinstance(obj, ServiceInterface) and command == "STOP":
            obj.stop()

        else:
            self.callNextHandler(obj, command)