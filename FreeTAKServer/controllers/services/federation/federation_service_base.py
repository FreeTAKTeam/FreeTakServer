from abc import ABC, abstractmethod

from FreeTAKServer.controllers.services.service_abstracts import ServerServiceInterface, ServiceBase

from FreeTAKServer.controllers.serializers.protobuf_serializer import ProtobufSerializer
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer

from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.SpecificCoT.SendDisconnect import SendDisconnect
from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent

class FederationServiceBase(ServerServiceInterface, ServiceBase):

    def _process_protobuff_to_object(self, protobuf_object: FederatedEvent):
        """ this method will convert the protobuf object to a FTS model object and xml string
        it will also add the remarks to indicate that the client or cot is comming from a federate

        Args:
            protobuf_object:

        Returns:

        """
        modelObject = XMLCoTController().determine_model_object_type(protobuf_object.event.type)
        fts_obj = ProtobufSerializer().from_format_to_fts_object(protobuf_object, modelObject())
        event = XmlSerializer().from_fts_object_to_format(fts_obj)
        """xmlstring = event
        if xmlstring.find('detail') and xmlstring.find('detail').
        xmlstring.find('detail').remove(xmlstring.find('detail').find('remarks'))
        xmlstring.find('detail').extend([child for child in xmlstring.find('detail')])"""
        return fts_obj, event

    def _get_header_length(self, header):
        return int.from_bytes(header, 'big')

    def _generate_header(self, contentlength):
        return contentlength.to_bytes(4, byteorder="big")

    def check_dest_user(self, data):
        """ this method is responsible for validating that the federate has
        any of the intended recipients for the CoT

        Args:
            data: a CoT object

        Returns boolean: True if the federate has any dest client otherwise false

        """
    def send_data_to_clients(self, data):
        from defusedxml import ElementTree as etree
        try:
            if self.federates:
                xmlstring = data.xmlString
                detail = etree.fromstring(xmlstring).find('detail')
                if detail:
                    protobuf = ProtobufSerializer().from_fts_object_to_format(data.modelObject)
                    try:
                        protobuf.event.other = etree.tostring(detail)
                        protobufstring = protobuf.SerializeToString()
                        header = self._generate_header(len(protobufstring))
                        protobufstring = header + protobufstring
                        print(protobufstring)
                    except Exception as e:
                        self.logger.warning("creating protobuf message failed "+str(e))
                        return None
                    for client in self.federates.values():
                        client.conn.send(protobufstring)
                else:
                    return None
            else:
                return None
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            self.logger.warning("sending data to federates failed "+str(e))

    def send_connection_data(self, CoT: ClientInformation) -> None:
        try:
            if self.federates:
                proto_obj = FederatedEvent()
                proto_obj.contact.uid = str(CoT.modelObject.uid)
                proto_obj.contact.callsign = str(CoT.modelObject.detail.contact.callsign)
                proto_obj.contact.operation = 1
                proto_str = proto_obj.SerializeToString()
                header = self._generate_header(len(proto_str))
                for fed in self.federates.values():
                    fed.conn.send(header + proto_str)
                return None
            else:
                return None

        except Exception as e:
            self.logger.warning("exception throw sending new connection data to federates " + str(e))
            return None

    def _send_connected_clients(self, connection):
        try:
            clients = self.db.query_user()
        except Exception as e:
            self.logger.warning("error thrown in getting clients from DataBase to send to federates " + str(e))
            return None
        for client in clients:
            try:
                proto_obj = FederatedEvent()
                proto_obj.contact.uid = str(client.uid)
                proto_obj.contact.callsign = str(client.CoT.detail.contact.callsign)
                proto_obj.contact.operation = 1
                proto_str = proto_obj.SerializeToString()
                header = self._generate_header(len(proto_str))
                connection.send(header+proto_str)
            except Exception as e:
                self.logger.warning("error thrown sending federate data to newly connected federate " + str(e))
                continue

    def disconnect_client(self, id: str) -> None:
        try:
            self.logger.info("disconnecting client")
            try:
                federate = self.federates[id]
            except Exception as e:
                self.logger.warning("federate array has no item with uid " + str(id) + " federates array is len " + str(
                    len(self.federates)))
                return None
            try:
                federate.conn.close()
                self.sel.unregister(federate.conn)
                del (self.federates[federate.uid])
            except Exception as e:
                self.logger.warning("exception thrown disconnecting client " + str(e))

            try:
                self.db.remove_ActiveFederation(f'id == "{federate.uid}"')
            except Exception as e:
                self.logger.warning("exception thrown removing outgoing federation from DB " + str(e))
            return None
        except Exception as e:
            self.logger.warning("exception thrown accessing client for disconnecting client " + str(e))

    def send_disconnection_data(self, CoT: SendDisconnect) -> None:
        if self.federates:
            proto_obj = FederatedEvent()
            proto_obj.contact.uid = str(CoT.modelObject.detail.link.uid)
            proto_obj.contact.callsign = str(CoT.modelObject.detail.link.type)
            proto_obj.contact.operation = 4
            proto_str = proto_obj.SerializeToString()
            header = self._generate_header(len(proto_str))
            for fed in self.federates.values():
                fed.conn.send(header + proto_str)
            return None
        else:
            return None