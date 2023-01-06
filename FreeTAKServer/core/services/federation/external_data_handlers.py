from FreeTAKServer.core.services.federation.handlers import HandlerBase

from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent

class FederationProtobufValidationHandler(HandlerBase):
    """
    this handler is responsible for validation that a passed command has the proper type for subsequent handlers
    """
    def Handle(self, obj, command):

        if isinstance(command, FederatedEvent):
            self.callNextHandler(obj, command)

        else:
            raise TypeError("this command chain only accepts Protobuf data of type FederatedEvent")

class FederationProtobufConnectionHandler(HandlerBase):
    """
    this handler is responsible for parsing connection data coming from a federate and adding it to the calling services user dictionary
    """
    def Handle(self, obj, command):
        if command.contact.operation == 1:
            obj.add_service_user(command)
            self.callNextHandler(obj, command)
        else:
            self.callNextHandler(obj,command)

class FederationProtobufDisconnectionHandler(HandlerBase):
    """
    this handler is responsible for parsing clients disconnection data coming from a federate
    """
    def Handle(self, obj, command):
        if command.contact.operation == 4:
            obj.remove_service_user(command)
            self.callNextHandler(obj, command)
        else:
            self.callNextHandler(obj, command)

class FederationProtobufStandardHandler(HandlerBase):
    """
    this handler is responsible for serializing client data and sharing it with FTS core
    """
    def Handle(self, obj, command):
        pass
        # serialized_data = obj.serialize_data(command)
        # obj.send_command_to_core(serialized_data)