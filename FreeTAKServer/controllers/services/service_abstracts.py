from abc import ABC, abstractmethod, abstractproperty
import queue

class ServiceInterface(ABC):

    @abstractmethod
    def start(self, Pipe):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

class ServiceBase(ServiceInterface):

    def receive_command_data(self, pipe: queue.Queue) -> any:
        if not pipe.empty():
            return pipe.get()
        else:
            return None

    @abstractmethod
    def _define_responsibility_chain(self):
        raise NotImplemented

class ServerServiceInterface(ServiceInterface):
    from FreeTAKServer.controllers.configuration.types import Types
    @abstractmethod
    def send_data_to_clients(self, sender, data: Types.fts_object):
        raise NotImplementedError

    @abstractmethod
    def disconnect_client(self, client):
        raise NotImplementedError

class ServerServiceAbstract(ServerServiceInterface, ServiceBase):
    @abstractmethod
    def _accept_connection(self, key):
        raise NotImplemented

    @abstractmethod
    def _receive_data_from_client(self, key):
        raise NotImplemented

    def _create_selector(self):
        from selectors import DefaultSelector
        sel = DefaultSelector()
        return sel