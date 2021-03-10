from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
import ssl
from FreeTAKServer.controllers.services.DataPackageServer import FlaskFunctions, Path, dp_directory, os, app, const
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.SSLSocketController import SSLSocketController
import time

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SSLDataPackageServer").getLogger()
from werkzeug.serving import make_server

class SSLDataPackageService(FlaskFunctions):
    def startup(self, ip, port, pipe, startuplock):
        try:
            time.sleep(3)
            import socket
            import ssl
            global IP, HTTPPORT
            startuplock.acquire(blocking=True)
            startuplock.acquire(blocking=False)
            IP = ip
            HTTPPORT = port
            PIPE = pipe
            # Make sure the data package directory exists
            if not Path(dp_directory).exists():
                # app.logger.info(f"Creating directory at {str(dp_directory)}")
                os.makedirs(str(dp_directory))
            # Create the relevant database tables
            print(const.IP)
            print(HTTPPORT)
            super().setIP(IP)
            super().setHTTPPORT(HTTPPORT)
            super().setPIPE(PIPE)
            self.SSLSocketController = SSLSocketController()
            self.SSLSocketController.changeIP(IP)
            self.SSLSocketController.changePort(HTTPPORT)
            startuplock.release()
            self.server = make_server(host=DataPackageServerConstants().IP, port=HTTPPORT, ssl_context=self.SSLSocketController.create_context(), app=app)
            self.server.serve_forever()

        except Exception as e:
            print(e)
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1
        
if __name__ == "__main__":
    SSLDataPackageService().startup('0.0.0.0', 8443)