from abc import ABC, abstractmethod
import multiprocessing
from typing import Dict, List
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.SQLAlchemy.User import User

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

    @abstractmethod
    def get_service_users(self) -> List[User]:
        """ the implementation of this method

        Returns Dict[str, ClientInformation]: a dictionary of client uid's and their associated objects

        """
        raise NotImplementedError

    def receive_command_data(self, pipe: multiprocessing.Pipe) -> any:
        if not pipe.empty():
            return pipe.get()
        else:
            return None

    def define_responsibility_chain(self):
        raise NotImplementedError