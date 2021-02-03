from queue import Queue
import socket
import ssl
from FreeTAKServer.controllers.services.FederationServiceAbstract import FederationServiceAbstract
from FreeTAKServer.controllers.services.FederationServiceController import FederationServiceController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("FederationClient").getLogger()


class FederationClientServiceController(FederationServiceAbstract):
    """this controller is instantiated upon the startup of FTS and is used to
    establish and control federations. this is NOT always running and has no while loops
    """

    def __init__(self, pipe):
        super().__init__(pipe)
        self.dataQueue = Queue()

    def create_client_federation(self, ip, port):
        try:
            sock = self._establish_connection(ip, port)
            federate = FederationServiceController(ip, port, sock).start()
            self.federateClients.add_client(federate)
        except Exception as e:
            logger.error(f"exception has been thrown in the creation of client federation { str(e) }")

    def remove_client_federation(self, Federate):
        pass

    def _establish_connection(self, ip, port):
        try:
            """TODO: add certificate validation using supplied CA note: in future FTS to FTS
                federation should use more secure cyphers for communication
            """
            # this function loads the ssl certificates and waits for a connection over the specified port
            # set TLSv1.2 as the version for communication
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

            # load the required certificates for authentication
            context.load_cert_chain(
                '/home/natha/ProgrammerStuff/FTS/FTSDev/FreeTAKServer/Certs/ServerCerts/testalpha.pem',
                '/home/natha/ProgrammerStuff/FTS/FTSDev/FreeTAKServer/Certs/ServerCerts/testalpha.key',
                password='atakatak')

            # downgrade to cyphers supported on TAKServer
            context.set_ciphers('DEFAULT@SECLEVEL=1')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = sock.connect((ip, port))
            ssock = context.wrap_socket(sock, server_hostname=ip)
            return ssock

        except Exception as e:
            logger.error('there has been an exception thrown in '
                         'the establishment of a client federation ' + str(e))

    def send(self, data):
        try:
            """
            a wrapper so that pipe method names can be used to interact
            with the class
            :param data:
            :return:
            """
            self.send_data_to_clients(data, self.federateClients.get_all_clients())
        except Exception as e:
            logger.error('there has been an exception throw in the sending '
                         'of data to a server this instance is federated to ' + str(e))
            raise e

    def recv(self):
        try:
            """
            a wrapper so that pipe method names can be used to interact
            with the class
            :return:
            """
            self.recv_data_from_clients(self.federateClients.get_all_clients())
        except Exception as e:
            logger.error('there has been an exception thrown in the reception '
                         'of data to a server this instance is federated to ' + str(e))
            raise e

    def poll(self):
        try:
            """
            a wrapper so that pipe method names can be used to interact
            with the class it calls the check_if_data_is_available method
            within FederationServiceAbstract and sends the returned data in
            pipe in
            :return:
            """
            data = self.check_if_data_is_available(self.federateClients.get_all_clients())
            if len(data) > 0:
                for CoT in data:
                    self.dataQueue.put(CoT)
                return True

            else:
                raise multiprocessing.TimeoutError
        except Exception as e:
            logger.error('there has been an exception thrown in the polling '
                         'of data to a server this instance is federated to ' + str(e))
            raise e

    def recv_data_from_clients(self, clients):
        from FreeTAKServer.model.ServiceObjects import Federate
        try:
            if isinstance(clients, list):
                for client in clients:
                    if isinstance(client, Federate):
                        for CoT in client.federationController.receive_data_from_federates():
                            self.dataQueue.put(CoT)

                    else:
                        raise TypeError('the list should only contain instances of the Federate class')
                return 1
            else:
                raise TypeError('this function should only be supplied a list object')
        except Exception as e:
            return -1


if __name__ == "__main__":
    import multiprocessing
    from FreeTAKServer.controllers import SendOtherController
    from FreeTAKServer.model.RawCoT import RawCoT
    import time
    temp = RawCoT()
    temp.type = None
    temp.clientInformation = None
    temp.protocol = None
    temp.xmlString = b'<event version="2.0" uid="123e915c-7b9a-44ed-91e7-5165e384b213" type="a-h-G" time="2020-09-02T00:15:50.504Z" start="2020-09-02T00:15:50.504Z" stale="2020-09-02T00:20:50.504Z" how="h-g-i-g-o"><point lat="28.31507" lon="-81.34564" hae="-5.185734847652469" ce="6.0" le="9999999.0"/><detail><contact callsign="2340 Cordova Ct, Kissimmee, FL 34743, USA"/><status readiness="true"/><archive/><link uid="ANDROID-863134036519299" production_time="2020-07-19T18:32:31.535Z" type="a-f-G-E-V-C" parent_callsign="WP4JMV" relation="p-p"/><remarks/><archive/><ce_human_input>true</ce_human_input><color argb="-1"/><_flow-tags_ TAK-Server-c0a2d13e="2020-09-01T12:32:01Z"/></detail></event>'
    a, b = multiprocessing.Pipe()
    # multiprocessing.Process(target=).start()
    FtsObject = SendOtherController(temp).getObject()
    # b.send(FtsObject)
    FederationClientServiceController(a, '192.168.2.105', 9000).start()
    time.sleep(1000)
    x = 1
    '''
    event {
  sendTime: 1598963344000
  startTime: 1599005949000
  staleTime: 1599006324000
  lat: 43.855695
  lon: -66.108016
  hae: 13.058658054176142
  ce: 58.9
  le: 9999999.0
  uid: "ANDROID-359975090666199"
  type: "a-f-G-U-C"
  coordSource: "h-e"
  other: "<detail><__group name=\"Yellow\" role=\"Team Member\"/><takv device=\"SAMSUNG SM-G950W\" platform=\"ATAK-CIV\" os=\"28\" version=\"4.0.0.1 (3a23eb4e).1585690033-CIV\"/><contact endpoint=\"*:-1:stcp\" phone=\"19027743142\" callsign=\"NOVA\"/><uid Droid=\"NOVA\"/><_flow-tags_ TAK-Server-c0a2d13e=\"2020-09-01T12:29:04Z\"/></detail>"
  battery: 48
  ploc: "GPS"
  palt: "GPS"
  course: 176.05777346688942
    }   '''
