from abc import ABC, abstractmethod
import multiprocessing


class ServiceInterface(ABC):

    @abstractmethod
    def start(self, Pipe):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError


class ServerServiceInterface(ServiceInterface):
    from FreeTAKServer.controllers.configuration.types import Types

    @abstractmethod
    def send_data_to_clients(self, data: Types.fts_object):
        raise NotImplementedError

    @abstractmethod
    def disconnect_client(self, client):
        raise NotImplementedError


class ServiceBase(ServiceInterface):

    def receive_command_data(self, pipe: multiprocessing.Pipe) -> any:
        if pipe.poll():
            return pipe.recv()
        else:
            return None

    def define_responsibility_chain(self):
        pass
