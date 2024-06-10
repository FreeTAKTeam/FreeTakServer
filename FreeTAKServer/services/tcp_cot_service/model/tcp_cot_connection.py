# direct import only to type hinting
from socket import socket
import copy

from digitalpy.core.IAM.model.connection import Connection

# direct import only to type hinting on line 20
from FreeTAKServer.components.core.fts_domain.domain import event

from ..configuration.tcp_cot_service_constants import SERVICE_NAME, XML

class TCPCoTConnection(Connection):
    def __init__(self, oid=None) -> None:
        super().__init__("tcp_cot_connection", oid)
        self._service_id = SERVICE_NAME
        self._protocol = XML
        self._model_object: event = None
        self._sock: socket = None
    
    @property
    def model_object(self):
        return self._model_object

    @model_object.setter
    def model_object(self, model_obj: event):
        self._model_object = model_obj

    @property
    def sock(self):
        return self._sock
    
    @sock.setter
    def sock(self, sock_new: socket):
        self._sock = sock_new

    # defined to avoid pickling the socket
    def __getstate__(self):
        state = self.__dict__
        state_cp = copy.copy(state)
        state_cp["_sock"] = None
        return state_cp
    
    def __str__(self):
        return f"{self._protocol}-{self._service_id}-{self._model_object.uid}"