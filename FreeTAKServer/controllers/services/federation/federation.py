from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.services.federation.handlers import StopHandler, DisconnectHandler, SendDataHandler, SendConnectionDataHandler, SendDisconnectionDataHandler
from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent
from FreeTAKServer.controllers.services.service_abstracts import ServerServiceInterface, ServiceBase
from FreeTAKServer.model.federate import Federate
import selectors
import socket
import ssl
import time
from FreeTAKServer.controllers.serializers.protobuf_serializer import ProtobufSerializer
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.model.SpecificCoT.SendOther import SendOther
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.SpecificCoT.SendDisconnect import SendDisconnect
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
logger = CreateLoggerController("FederationServer").getLogger()


class FederationServerService(ServerServiceInterface, ServiceBase):

    def __init__(self):
        self._define_responsibility_chain()
        self.pipe = None
        self.federates: {str: Federate} = {}
        self.sel = selectors.DefaultSelector()

    def _send_connected_clients(self, connection):
        try:
            clients = self.db.query_user()
        except Exception as e:
            logger.warning("error thrown in getting clients from DataBase to send to federates " + str(e))
            return None
        for client in clients:
            try:
                proto_obj = FederatedEvent()
                proto_obj.contact.uid = str(client.uid)
                proto_obj.contact.callsign = str(client.CoT.detail.contact.callsign)
                proto_obj.contact.operation = 1
                proto_str = proto_obj.SerializeToString()
                header = self._generate_header(len(proto_str))
                connection.send(header + proto_str)
            except Exception as e:
                logger.warning("error thrown sending federate data to newly connected federate " + str(e))
                continue

    def _create_context(self) -> None:
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(MainConfig.federationCert, MainConfig.federationKey,
                                     password=MainConfig.federationKeyPassword)

    def _create_listener(self, ip: str, port: int) -> None:
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
        from lxml import etree
        while True:
            time.sleep(0.1)
            command = self.receive_command_data(self.pipe)
            if command:
                try:
                    self.m_SendConnectionHandler.Handle(self, command)
                except Exception as e:
                    pass
            else:
                pass
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
                        detail = etree.fromstring(protobuf_object.event.other)
                        protobuf_object.event.other = ''
                        fts_obj = ProtobufSerializer().from_format_to_fts_object(protobuf_object, Event.FederatedCoT())
                        specific_obj = SendOther()
                        event = XmlSerializer().from_fts_object_to_format(fts_obj)
                        xmlstring = event
                        xmlstring.find('detail').remove(xmlstring.find('detail').find('remarks'))
                        xmlstring.find('detail').extend([child for child in detail])
                        # specific_obj.xmlString = etree.tostring(xmlstring)
                        print(etree.tostring(xmlstring))
                        specific_obj.xmlString = etree.tostring(xmlstring)
                        self.pipe.send(specific_obj)
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
            logger.warning("exception in receiving data from federate " + str(e))
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

            self.db.create_ActiveFederation(id=data.uid, federate="unknown", address=addr[0], port=addr[1], initiator="Remote")
            return None
        except Exception as e:
            print(e)
            logger.warning("exception thrown accepting federation " + str(e))

    def _get_header_length(self, header):
        return int.from_bytes(header, 'big')

    def _generate_header(self, contentlength):
        return contentlength.to_bytes(4, byteorder="big")

    def send_data_to_clients(self, data):
        from lxml import etree
        try:
            if self.federates:
                xmlstring = data.xmlString
                detail = etree.fromstring(xmlstring).find('detail')
                protobuf = ProtobufSerializer().from_fts_object_to_format(data.modelObject)
                protobuf.event.other = etree.tostring(detail)
                protobufstring = protobuf.SerializeToString()
                header = self._generate_header(len(protobufstring))
                protobufstring = header + protobufstring
                print(protobufstring)
                for client in self.federates.values():
                    client.conn.send(protobufstring)
            else:
                return None
        except Exception as e:
            logger.warning("send data to clients failed with exception " + str(e))

    def disconnect_client(self, id: str) -> None:
        try:
            logger.info("disconnecting client")
            try:
                federate = self.federates[id]
            except Exception as e:
                logger.warning("federate array has no item with uid " + str(id) + " federates array is len " + str(
                    len(self.federates)))
                return None
            try:
                federate.conn.close()
                self.sel.unregister(federate.conn)
                del (self.federates[federate.uid])
            except Exception as e:
                logger.warning("exception thrown disconnecting client " + str(e))

            try:
                self.db.remove_ActiveFederation(f'id == "{federate.uid}"')
            except Exception as e:
                logger.warning("exception thrown removing outgoing federation from DB " + str(e))
            return None
        except Exception as e:
            logger.warning("exception thrown accessing client for disconnecting client " + str(e))

    def send_connection_data(self, CoT: ClientInformation):
        if self.federates:
            proto_obj = FederatedEvent()
            proto_obj.contact.uid = str(CoT.modelObject.uid)
            proto_obj.contact.callsign = str(CoT.modelObject.detail.contact.callsign)
            proto_obj.contact.operation = 1
            proto_str = proto_obj.SerializeToString()
            header = self._generate_header(len(proto_str))
            for fed in self.federates.values():
                fed.conn.send(header + proto_str)
        else:
            return None

    def send_disconnection_data(self, CoT: SendDisconnect):
        if self.federates:
            proto_obj = FederatedEvent()
            proto_obj.contact.uid = str(CoT.modelObject.detail.link.uid)
            proto_obj.contact.callsign = str(CoT.modelObject.detail.link.type)
            proto_obj.contact.operation = 4
            proto_str = proto_obj.SerializeToString()
            header = self._generate_header(len(proto_str))
            for fed in self.federates.values():
                fed.conn.send(header + proto_str)
        else:
            return None

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
