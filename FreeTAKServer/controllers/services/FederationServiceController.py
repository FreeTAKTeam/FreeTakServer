from multiprocessing import TimeoutError
from FreeTAKServer.controllers.FederatedCoTController import FederatedCoTController
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent
import codecs
import socket
from FreeTAKServer.model.ServiceObjects.Federate import Federate


class FederationServiceController:
    def __init__(self, ip, port, connection):
        self.ip = ip
        self.port = port
        self.pool = None
        self.buffer = 4
        self.excessData = None
        self.killSwitch = False
        self.connection = connection

    def start(self):

        federateObject = Federate()
        federateObject.federationController = self
        federateObject.IP = self.connection.getpeername()[0]
        federateObject.Port = self.connection.getpeername()[1]
        federateObject.Socket = self.connection
        return federateObject

    def establish_connection(self, ip, port):
        # returns a socket object
        pass

    def disconnect(self):
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            return 1
        except BaseException:
            self.connection.close()
            return 1

    def generate_header(self, contentlength):
        tempHex = format(contentlength, 'x')
        if (len(tempHex) % 2) == 0:
            filteredhex = [(tempHex[i:i + 2]) for i in range(0, len(tempHex), 2)]
            while len(filteredhex) < 4:
                filteredhex.insert(0, '00')
            filteredhex = r'\x'.join(filteredhex)
            filteredhex = r'\x' + filteredhex
            filteredhex = codecs.escape_decode(filteredhex)[0]
            return filteredhex
        else:
            tempHex = '0' + tempHex
            filteredhex = [(tempHex[i:i + 2]) for i in range(0, len(tempHex), 2)]
            while len(filteredhex) < 4:
                filteredhex.insert(0, '00')
            filteredhex = r'\x'.join(filteredhex)
            filteredhex = r'\x' + filteredhex
            filteredhex = codecs.escape_decode(filteredhex)[0]
            return filteredhex

    def get_header_length(self, header):
        try:
            from binascii import hexlify
            headerInHex = header.split(b'\\x')
            if len(headerInHex[-1]) == 3:
                headerInHex[-1][2] = hexlify(headerInHex[-1][2])
            headerInHex = b''.join(headerInHex)
            return int(headerInHex, 16)
        except BaseException:
            return -1

    def receive_data_from_federates(self):
        # returns data received from federate
        # the following logic receives data from the federate and processes the protobuf
        # up to 100 CoT's
        dataCount = 0
        dataArray = []
        # 100 is the limit of data which can be received from a federate in one iteration
        while dataCount < 100:
            dataCount += 1
            try:
                try:
                    self.connection.settimeout(0.01)
                    data = self.connection.recv(self.buffer)
                    self.connection.settimeout(0)
                except TimeoutError:
                    break

                except Exception as e:
                    self.disconnect()
                    self.killSwitch = True
                    return 0
                if data != [b'']:
                    header = data[0]
                    content = self.connection.recv(self.get_header_length(header))
                    EmptyFTSObject = Event.FederatedCoT()
                    protoObject = FederatedEvent().FromString(content)
                    print(protoObject)
                    FTSObject = FederatedCoTController().serialize_main_contentv1(protoObject, EmptyFTSObject)
                    print('received data from Federate')
                    print(content)
                else:
                    self.killSwitch = True

                dataArray.append(FTSObject)

            except Exception as e:
                pass

    def send_data_to_federates(self, data):
        try:

            # sends supplied data to supplied socket upon being called
            federatedEvent = FederatedEvent()
            ProtoObj = FederatedCoTController().serialize_from_FTS_modelv1(federatedevent=federatedEvent, ftsobject=data)
            protostring = ProtoObj.SerializeToString()
            header = self.generate_header(len(protostring))
            protostring = header + protostring
            print(b'sent ' + protostring + b' to federate')
            self.connection.send(protostring)
            return 1

        except Exception as e:
            pass

    def recv_in_data_pipe(self, pipe):
        pass

    def send_in_data_pipe(self, pipe, data):
        pass


if __name__ == '__main__':
    FederationServiceController
    content = b'\n\xb1\x06\x08\xd8\x81\xa6\xa1\xec.\x10\x84\xf0\xa5\xa1\xec.\x18\x84\xa8\xbf\xca\xec.1\x00\x00\x00\xe0\xcf\x12cA9\x00\x00\x00\xe0\xcf\x12cAA\x00\x00\x00\xe0\xcf\x12cAJjGeoChat.S-1-5-21-2720623347-3037847324-4167270909-1002.All Chat Rooms.673a0aa4-c8eb-4bb5-aa7e-abab7d8d89a0R\x05b-t-fZ\th-g-i-g-ob\x80\x05<detail><__chat id="All Chat Rooms" chatroom="All Chat Rooms" senderCallsign="FEATHER" groupOwner="false"><chatgrp id="All Chat Rooms" uid0="S-1-5-21-2720623347-3037847324-4167270909-1002" uid1="All Chat Rooms"/></__chat><link uid="S-1-5-21-2720623347-3037847324-4167270909-1002" type="a-f-G-U-C-I" relation="p-p"/><remarks source="BAO.F.WinTAK.S-1-5-21-2720623347-3037847324-4167270909-1002" sourceID="S-1-5-21-2720623347-3037847324-4167270909-1002" to="All Chat Rooms" time="2021-01-02T17:33:40.74Z">aa</remarks><_flow-tags_ TAK-Server-c0581fed97ff4cb89eb8666a8794670cc9f77ddb-badf-48da-abe7-84545ecda69d="2021-01-02T17:33:43Z"/></detail>'
    y = FederatedEvent().FromString(content)
    1 == 1
