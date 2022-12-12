from FreeTAKServer.controllers.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants

from .DataPackageServer import (
    FlaskFunctions, Path, app, const, dp_directory, eventlet, os)

loggingConstants = LoggingConstants(log_name="FTS-TCP_DataPackage_Service")
logger = CreateLoggerController("FTS-TCP_DataPackage_Service", logging_constants=loggingConstants).getLogger()

class TCPDataPackageService(FlaskFunctions):
    def startup(self, ip, port, pipe):
        try:
            from eventlet import wsgi
            global IP, HTTPPORT, PIPE
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
            super().setHTTPPORT(HTTPPORT)
            super().setIP(IP)
            super().setPIPE(PIPE)
            wsgi.server(eventlet.listen((DataPackageServerConstants().IP, HTTPPORT)), app)


        except Exception as e:
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1
