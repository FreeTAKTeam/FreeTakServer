from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
import ssl
from FreeTAKServer.controllers.services.DataPackageServer import FlaskFunctions, Path, dp_directory, os, app, eventlet, const
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.SSLSocketController import SSLSocketController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SSLDataPackageServer").getLogger()

class SSLDataPackageService(FlaskFunctions):
    def startup(self, ip, port, pipe):
        try:
            from eventlet import wsgi, wrap_ssl, listen
            import socket
            import ssl
            from FreeTAKServer.controllers.MainSocketController import MainSocketController
            from FreeTAKServer.model.sockets.SSLServerSocket import SSLServerSocket
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
            #wsgi.server(eventlet.listen(('', 14533)), app)  keyfile=MainConfig.keyDir,
            self.SSLSocketController = SSLSocketController()
            self.SSLSocketController.changeIP(IP)
            self.SSLSocketController.changePort(HTTPPORT)
            self.setSSL(True)
            wsgi.server(sock=wrap_ssl(listen((DataPackageServerConstants().IP, int(HTTPPORT))), keyfile=MainConfig.unencryptedKey,
                                      certfile=MainConfig.pemDir,
                                      server_side=True, ca_certs=MainConfig.CA), site=app)
        except Exception as e:
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1
        
if __name__ == "__main__":
    SSLDataPackageService().startup('0.0.0.0', 8443)