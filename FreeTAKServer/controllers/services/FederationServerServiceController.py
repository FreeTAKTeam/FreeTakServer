from FreeTAKServer.controllers.services.FederationServiceController import FederationServiceController
from FreeTAKServer.controllers.services.FederationServiceAbstract import FederationServiceAbstract
import ssl
import multiprocessing
import socket
import threading
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("FederationServer").getLogger()

class FederationServerServiceController(FederationServiceAbstract):

    """this service acts as both an orchestrator for the connection of new clients and
    an abstraction layer between FTS and all clients for the transfer of data. and is
    always running.
    """

    def listen_for_connection(self, ip, port, ssock):
        '''
        listens for connection
        :param ip:
        :param port:
        '''
        while True:
            try:
                conn, addr = ssock.accept()
                federate = self.connected(ip, port, conn)
            except Exception as e:
                logger.error("there has been an exception in listening for connections "
                             "within the reception of Federates " + str(e))

    def connected(self, ip, port, conn):
        try:
            '''
            this function handles connecting federates
            :return:
            '''
            federate = FederationServiceController(ip, port, conn).start()
            self.federateClients.add_client(federate)
            return federate
        except Exception as e:
            logger.error('there has been an exception in the '
                         'processing of a client connection'
                         ' within the connect function ' + str(e))

    def start(self, ip, port):
        try:
            '''
            the main start function which controls all other threads
            :param ip:
            :param port:
            :return:
            '''
            ssock = self._create_socket(ip, port)
            self.data_handler_thread = threading.Thread(target=self.data_handler, args=())
            self.data_handler_thread.start()
            self.listen_for_connection(ip, port, ssock)
        except Exception as e:
            logger.error('there has been an exception in the starting of the server'
                         ' Federation Service ' + str(e))

    def _create_socket(self, ip, port):
        try:
            # TODO: move certificate location and password to configuration
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain('/home/natha/ProgrammerStuff/FTS/FTSDev/FreeTAKServer/Certs/ServerCerts/server.crt',
                                    '/home/natha/ProgrammerStuff/FTS/FTSDev/FreeTAKServer/Certs/ServerCerts/server.key',
                                    password='atakatak')
            # context.load_cert_chain(r'C:\Users\natha\Documents\programmer_stuff\playground\CERT\TAKServerCerts\FTS certs\fts-server-cert.pem', r'C:\Users\natha\Documents\programmer_stuff\playground\CERT\TAKServerCerts\FTS certs\fts-server-key.key',password='ftsfts')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            sock.bind((ip, port))
            sock.listen(5)
            ssock = context.wrap_socket(sock, server_side=True)
            return ssock
        except Exception as e:
            logger.error('there has been an exception in the creation'
                         ' of the server socket ' + str(e))

    def data_handler(self):
        '''
        this function controlls the sending and receiving of data
        via the pipe passed in startup and is run in a thread
        :return:
        '''
        while True:
            try:
                self.pipe.poll(timeout = 0.01)
                success = self.send_data_to_clients(self.pipe.get(), self.federateClients.get_all_clients())
            except multiprocessing.TimeoutError:
                pass
            except Exception as e:
                logger.error('there has been an exception in the sending of'
                             ' data from pipe to federate clients ' + str(e))

            try:
                success = self.recv_data_from_clients(self.federateClients.get_all_clients())
            except Exception as e:
                logger.error('there has been an exception in the reception of'
                             ' data from pipe to federate clients ' + str(e))
