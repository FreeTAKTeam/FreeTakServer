from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
import ssl
from FreeTAKServer.controllers.services.DataPackageServer import FlaskFunctions, Path, os, app, eventlet, const, init_config
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.SSLSocketController import SSLSocketController

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

loggingConstants = LoggingConstants(log_name="FTS-SSL_DataPackage_Service")
logger = CreateLoggerController("FTS-SSL_DataPackage_Service", logging_constants=loggingConstants).getLogger()

class SSLDataPackageService(FlaskFunctions):
    def startup(self, ip, port, pipe):
        try:
            from eventlet import wsgi, wrap_ssl, listen
            import socket
            import ssl
            from FreeTAKServer.controllers.MainSocketController import MainSocketController
            from FreeTAKServer.model.sockets.SSLServerSocket import SSLServerSocket
            global IP, HTTPPORT
            init_config()
            self.MainSocket = SSLServerSocket()
            IP = ip
            HTTPPORT = port
            PIPE = pipe
            # Make sure the data package directory exists
            # Create the relevant database tables
            print(const.IP)
            print(HTTPPORT)
            super().setIP(IP)
            super().setHTTPPORT(HTTPPORT)
            super().setPIPE(PIPE)
            #wsgi.server(eventlet.listen(('', 14533)), app)  keyfile=config.keyDir,
            self.SSLSocketController = SSLSocketController()
            self.SSLSocketController.changeIP(IP)
            self.SSLSocketController.changePort(HTTPPORT)
            self.setSSL(True)
            wsgi.server(sock=wrap_ssl(listen((DataPackageServerConstants().IP, int(HTTPPORT))), keyfile=config.unencryptedKey,
                                      certfile=config.pemDir,
                                      server_side=True, ca_certs=config.CA, cert_reqs=ssl.CERT_REQUIRED), site=app)
        except Exception as e:
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1
