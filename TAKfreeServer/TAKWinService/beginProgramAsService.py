import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import os.path
import threading
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from server import ThreadedServer
class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "TAKServer"
    _svc_display_name_ = "TAKServer"
    killSwitch = 0

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.killSwitch = 1

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_,''))
        self.main()

    def main(self):
        t = threading.Thread(target = ThreadedServer('',8087).listen, args = (), daemon=True)
        t.start()
        while True:
            if self.killSwitch == 1:
                sys.exit()
            else:
                True

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
