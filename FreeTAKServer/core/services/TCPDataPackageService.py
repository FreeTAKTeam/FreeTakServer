from digitalpy.core.main.object_factory import ObjectFactory

from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants

from .DataPackageServer import (
    FlaskFunctions, app, const, eventlet, init_config)

loggingConstants = LoggingConstants(log_name="FTS-TCP_DataPackage_Service")
logger = CreateLoggerController("FTS-TCP_DataPackage_Service", logging_constants=loggingConstants).getLogger()

class TCPDataPackageService(FlaskFunctions):
    def startup(self, ip, port, pipe, factory):
        try:
            from eventlet import wsgi
            global IP, HTTPPORT, PIPE
            IP = ip
            HTTPPORT = port
            PIPE = pipe
            ObjectFactory.configure(factory)
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
