from .DataPackageServer import FlaskFunctions, Path, os, app, eventlet, const, init_config
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants

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
            init_config()
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