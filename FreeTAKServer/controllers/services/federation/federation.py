from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.configuration.types import Types
from FreeTAKServer.controllers.services.federation.handlers import StopHandler, DisconnectHandler, ConnectHandler, SendDataHandler, SendConnectionDataHandler, SendDisconnectionDataHandler
from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent
from FreeTAKServer.controllers.services.service_abstracts import ServerServiceInterface, ServiceBase
from multiprocessing import Pipe as multiprocessingPipe
from FreeTAKServer.model.federate import Federate
import selectors
import socket
from typing import Tuple
import ssl
import time
import codecs
from FreeTAKServer.controllers.serializers.protobuf_serializer import ProtobufSerializer
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.model.SpecificCoT.SendOther import SendOther
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
import threading
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.SpecificCoT.SendDisconnect import SendDisconnect
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
loggingConstants = LoggingConstants(log_name="FTS_FederationServerService")
logger = CreateLoggerController("FTS_FederationServerService", logging_constants=loggingConstants).getLogger()
from defusedxml import ElementTree as etree

loggingConstants = LoggingConstants()


from FreeTAKServer.controllers.services.federation.federation_service_base import FederationServiceBase

class FederationServerService(FederationServiceBase):

    def __init__(self):
        self._define_responsibility_chain()
        self.pipe = None
        self.federates: {str: Federate} = {}
        self.sel = selectors.DefaultSelector()
        self.logger = logger

    def _create_context(self) ->None:
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(MainConfig.federationCert, MainConfig.federationKey,
                                     password=MainConfig.federationKeyPassword)

    def _create_listener(self, ip: str, port: int)->None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind((ip, port))
        sock.listen()
        ssock = self.context.wrap_socket(sock, server_side=True)
        ssock.setblocking(False)
        self.sel.register(ssock, selectors.EVENT_READ, data=None)

    def _define_responsibility_chain(self):
        self.m_StopHandler = StopHandler()

        self.m_DisconnectHandler = DisconnectHandler()
        self.m_DisconnectHandler.setNextHandler(self.m_StopHandler)

        self.m_SendDataHandler = SendDataHandler()
        self.m_SendDataHandler.setNextHandler(self.m_DisconnectHandler)

        self.m_SendDisconnectionHandler = SendDisconnectionDataHandler()
        self.m_SendDisconnectionHandler.setNextHandler(self.m_SendDataHandler)

        # first handler in chain of responsibility and should be called first
        self.m_SendConnectionHandler = SendConnectionDataHandler()
        self.m_SendConnectionHandler.setNextHandler(self.m_SendDisconnectionHandler)

    def main(self):
        inbound_data_thread = threading.Thread(target=self.inbound_data_handler)
        inbound_data_thread.start()
        outbound_data_thread = threading.Thread(target=self.outbound_data_handler)
        outbound_data_thread.start()
        inbound_data_thread.join()

    def outbound_data_handler(self):
        """ this is the main process respoonsible for receiving data from federates and sharing
        with FTS core

        Returns:

        """
        while True:
            try:
                data = self.receive_data_from_federate(1)
            except ssl.SSLWantReadError:
                data = None
            if data:
                for protobuf_object in data:
                    # TODO: clean all of this up as it's just a PoC

                    # event = etree.Element('event')
                    # SpecificCoTObj = XMLCoTController().categorize_type(protobuf_object.type)
                    try:
                        specific_obj, xmlstring = self._process_protobuff_to_object(protobuf_object)
                        # specific_obj.xmlString = etree.tostring(xmlstring)
                        specific_obj.xmlString = etree.tostring(xmlstring)
                        if self.pipe.sender_queue.full():
                            print('queue full !!!')
                        self.pipe.put(specific_obj)
                        print("data put in pipe " + str(etree.tostring(xmlstring)))
                    except Exception as e:
                        pass
                    """if isinstance(SpecificCoTObj, SendOtherController):
                        detail = protobuf_object.event.other
                        protobuf_object.event.other = ''
                        fts_obj = ProtobufSerializer().from_format_to_fts_object(protobuf_object, Event.Other())
                        protobuf_object.event.other = detail
                        SpecificCoTObj.object = fts_obj
                        SpecificCoTObj.Object =
                    else:
                        fts_obj = ProtobufSerializer().from_format_to_fts_object(protobuf_object, SpecificCoTObj().object)
                        self.pipe.send(data)"""
            else:
                pass
    def inbound_data_handler(self):
        """this is the main process responsible for receiving data from FTS core

        Returns:

        """
        while True:
            try:
                command = self.receive_command_data(self.pipe)
                if command:
                    try:
                        self.m_SendConnectionHandler.Handle(self, command)
                    except Exception as e:
                        pass
                else:
                    pass
            except Exception as e:
                self.logger.error(str(e))
    def receive_data_from_federate(self, timeout):
        """called whenever data is available from any federate and immediately proceeds to
        send data through process pipe
        """
        dataarray = []
        events = self.sel.select(timeout)
        for key, mask in events:
            if key.data is None:
                self._accept_connection(key.fileobj)
            else:
                federate_data = self._receive_new_data(key)
                if federate_data:
                    dataarray.append(federate_data)
        return dataarray

    def _receive_new_data(self, key):
        try:
            conn = key.fileobj
            header = conn.recv(4)
            if header:
                try:
                    buffer = self._get_header_length(header)
                    raw_protobuf_message = conn.recv(buffer)
                    print(raw_protobuf_message)
                    protobuf_object = FederatedEvent()
                    protobuf_object.ParseFromString(raw_protobuf_message)
                    return protobuf_object
                except Exception as e:
                    conn.recv(10000)
                    return None
            else:
                self.disconnect_client(key.data.uid)
        except OSError:
            return None
        except Exception as e:
            self.logger.warning("exception in receiving data from federate "+str(e))
            self.disconnect_client(key.data.uid)
    
    def _accept_connection(self, sock) -> None:
        try:
            import uuid
            conn, addr = sock.accept()  # Should be ready to read
            print('accepted connection from', addr)
            conn.setblocking(False)
            data = Federate()
            data.conn = conn
            # get federate certificate CN
            # data.name = dict(x[0] for x in conn.getpeercert()["subject"])["commonName"]
            data.name = addr[0]
            data.addr = addr
            data.uid = str(uuid.uuid4())
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            self._send_connected_clients(conn)
            self.sel.register(conn, events, data=data)
            self.federates[data.uid] = data

            self.db.create_ActiveFederation(id = data.uid, federate = "unknown", address = addr[0], port = addr[1], initiator = "Remote")
            return None
        except Exception as e:
            print(e)
            self.logger.warning("exception thrown accepting federation " + str(e))

    def start(self, pipe, ip, port):
        self.db = DatabaseController()
        self.pipe = pipe
        self._create_context()
        self._create_listener(ip, port)
        print('started federation server service')
        self.main()

    def stop(self):
        pass

if __name__ == "__main__":

    from multiprocessing import Pipe
    pipe1, pipe2 = Pipe(True)
    FederationServerService().start(pipe1, "0.0.0.0", 9000)
