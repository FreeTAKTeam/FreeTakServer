import ssl

from eventlet import listen, wrap_ssl, wsgi
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.connection.SSLSocketController import SSLSocketController
from FreeTAKServer.controllers.services.DataPackageServer import (
    FlaskFunctions, Path, app, const, dp_directory, os)
from FreeTAKServer.model.sockets.SSLServerSocket import SSLServerSocket

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

loggingConstants = LoggingConstants(log_name="FTS-SSL_DataPackage_Service")
logger = CreateLoggerController("FTS-SSL_DataPackage_Service", logging_constants=loggingConstants).getLogger()

class SSLDataPackageService(FlaskFunctions):
    def startup(self, ip, port, pipe):
        try:
            global IP, HTTPPORT
            self.MainSocket = SSLServerSocket()
            IP = ip
            HTTPPORT = port
            PIPE = pipe
            # Make sure the data package directory exists
            if not Path(dp_directory).exists():
                app.logger.info(f"Creating directory at {str(dp_directory)}")
                os.makedirs(str(dp_directory))
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
