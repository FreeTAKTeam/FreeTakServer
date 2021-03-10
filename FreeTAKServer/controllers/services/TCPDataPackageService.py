from FreeTAKServer.controllers.services.DataPackageServer import FlaskFunctions, Path, dp_directory, os, app, const
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
import time

loggingConstants = LoggingConstants()
logger = CreateLoggerController("TCPDataPackageServer").getLogger()
from waitress import serve
#monkey.patch_all()
import cheroot
from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
print(cheroot.__version__)
import os
# from gevent.pywsgi import WSGIServer
class TCPDataPackageService(FlaskFunctions):
    def startup(self, ip, port, pipe, startuplock):
        try:
            # from gevent.pywsgi import WSGIServer
            global IP, HTTPPORT, PIPE
            #startuplock.acquire(blocking=True)
            #startuplock.acquire(blocking=False)
            time.sleep(3)
            IP = ip
            HTTPPORT = port
            PIPE = pipe
            # Make sure the data package directory exists
            if not Path(dp_directory).exists():
                #app.logger.info(f"Creating directory at {str(dp_directory)}")
                os.makedirs(str(dp_directory))
            # Create the relevant database tables
            print(const.IP)
            print(HTTPPORT)
            super().setHTTPPORT(HTTPPORT)
            super().setIP(IP)
            super().setPIPE(PIPE)
            #startuplock.release()
            time.sleep(1)
            # from werkzeug.debug import DebuggedApplication
            # DebuggedApplication()
            d = PathInfoDispatcher({'/': app})
            self.server = WSGIServer((DataPackageServerConstants().IP, HTTPPORT), d)
            # self.server = serve(host=DataPackageServerConstants().IP, port=HTTPPORT, app=app)
            self.server.start()

        except Exception as e:
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1
if __name__ == "__main__":
    import threading
    def start():
        threading.Thread(target=TCPDataPackageService().startup, args=("0.0.0.0", 8080, 123, threading.Lock())).start()
    threading.Thread(target=start).start()
    time.sleep(10)