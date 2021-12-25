from abc import ABC

from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.federate import Federate
from FreeTAKServer.model.clients import ClientAbstract
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.SpecificCoT.SpecificCoTAbstract import SpecificCoTAbstract
from FreeTAKServer.model.SpecificCoT.SendOther import SendOther

from FreeTAKServer.controllers.services.service_abstracts import ServerServiceInterface, ServiceInterface
from FreeTAKServer.controllers.services.federation.federation_service_base import FederationServiceBase
from FreeTAKServer.controllers.configuration.types import Types
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

    def Handle(self, obj: FederationServiceBase, command):
        raise NotImplementedError

    def setNextHandler(self, handler: HandlerInterface):
        """ set next handler to be called in chain of responsibility

        :params handler: the handler which should be next in chain of responsibility
        """

        self.nextHandler = handler

    def callNextHandler(self, obj: FederationServiceBase, command):
        if self.nextHandler is None:
            raise Exception("no further handlers, object not supported by responsibility chain")
        else:
            self.nextHandler.Handle(obj, command)

# service level command handlers below

class StopHandler(HandlerBase):
    """ Handler for command stop service

    """

    def Handle(self, obj: FederationServiceBase, command):

        if isinstance(obj, FederationServiceBase) and command == "STOP":
            obj.stop()

        else:
            self.callNextHandler(obj, command)

# connection level command handlers below

class ConnectHandler(HandlerBase):
    """ Handler for command to connect to new server

    """

    def Handle(self, obj: FederationServiceBase, command):
        if isinstance(command, tuple) and command[1] == "CREATE":
            obj.connect_to_server(command)

        else:
            self.callNextHandler(obj, command)


class DisconnectHandler(HandlerBase):
    """ Handler for command to disconnect client

    """

    def Handle(self, obj: FederationServiceBase, command):
        if isinstance(obj, FederationServiceBase) and isinstance(command, tuple) and command[1] == "DELETE":
            obj.disconnect_client(command[0])

        else:
            self.callNextHandler(obj, command)


# Data level command handlers below

class DestinationValidationHandler(HandlerBase):
    """
    this handler is responsible for validating that the desired destination of a CoT
    is present before being sent
    """

    def Handle(self, obj: FederationServiceBase, command: SpecificCoTAbstract) -> None:
        user_list = obj.get_service_users()
        if isinstance(command.modelObject, SendOther):
            if command.modelObject.martiPresent:

                user_callsigns = [user.contact.callsign for user in user_list]
                cot_dest_callsigns = [dest.callsign for dest in command.modelObject.detail.marti.dest]

                if bool(set(user_callsigns) & set(cot_dest_callsigns)):
                    self.callNextHandler(obj, command)
                else:
                    raise Exception("this service has none of the desired clients for this CoT")

        elif hasattr(command.modelObject.detail, 'marti') and hasattr(command.modelObject.detail.marti.dest[0], 'callsign'):
            user_callsigns = [user.contact.callsign for user in user_list]
            cot_dest_callsigns = [dest.callsign for dest in command.modelObject.detail.marti.dest]

            if bool(set(user_callsigns) & set(cot_dest_callsigns)):
                self.callNextHandler(obj, command)
            else:
                raise Exception("this service has none of the desired clients for this CoT")
        else:
            self.callNextHandler(obj, command)


class DataValidationHandler(HandlerBase):
    """this handler is responsible for validating that the contents of a data object
    are of proper type and contain basic required attributes
    """

    def Handle(self, obj, command):
        # validate data
        if isinstance(command, SpecificCoTAbstract) or isinstance(command, ClientInformation):
            self.callNextHandler(obj, command)
        else:
            raise TypeError('invalid command content for data level handler')

class SendDataHandler(HandlerBase):
    """ Handler for command send data to client, should always be the final handler in the data_handler_chain of any class

    """

    def Handle(self, obj: FederationServiceBase, command: any):

        if isinstance(obj, FederationServiceBase) and isinstance(command, SpecificCoTAbstract):
            obj.send_data_to_clients(command)

        else:
            self.callNextHandler(obj, command)


class SendConnectionDataHandler(HandlerBase):
    """ handler for command send client connection data to federate

    """

    def Handle(self, obj: FederationServiceBase, command: any):

        if isinstance(obj, FederationServiceBase) and isinstance(command, ClientInformation):
            obj.send_connection_data(command)
            return None
        else:
            self.callNextHandler(obj, command)


class SendDisconnectionDataHandler(HandlerBase):
    """ handler for command send client disconnection data to federate

    """

    def Handle(self, obj: ServiceInterface, command):
        from FreeTAKServer.model.SpecificCoT.SendDisconnect import SendDisconnect

        if isinstance(obj, FederationServiceBase) and isinstance(command, SendDisconnect):
            obj.send_disconnection_data(command)

        else:
            self.callNextHandler(obj, command)
