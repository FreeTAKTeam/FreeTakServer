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
import argparse
import logging
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from server import ThreadedServer
ThreadedServer()
import time
import random
from pathlib import Path
from SMWinservice import SMWinservice
class PythonCornerExample(SMWinservice):
    _svc_name_ = "PythonCornerExample"
    _svc_display_name_ = "Python Corner's Winservice Example"
    _svc_description_ = "That's a great winservice! :)"
    logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        logging.debug('main init')
        t = threading.Thread(target = ThreadedServer().listen, daemon=True)
        t.start()
        while self.isrunning:
            pass
        sys.exit()
if __name__ == '__main__':
    PythonCornerExample.parse_command_line()

'''
class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "FreeTAKServer"
    _svc_display_name_ = "FreeTAKServer"
    logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')
    logging.debug('primary run')

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args, ip = None, port = None)
        logging.debug(ip+' and '+str(port))
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        logging.debug('init startup')
        
        self.killSwitch = 0

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.killSwitch = 1

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_,''))
        logging.debug('svcDoRun startup')
        self.main()

    def main(self):
        global ip
        global port
        import server
        t = threading.Thread(target = server.ThreadedServer(self.ip,self.port).listen, args = (), daemon=True)
        t.start()
        while True:
            if self.killSwitch == 1:
                sys.exit()
            else:
                True

if __name__ == '__main__':
    if sys.argv[1] == 'start':
        ip = input('please enter your server IP: ')

        port = int(input('please enter the port your server should be listening on: '))
        win32serviceutil.HandleCommandLine(AppServerSvc, ip = ip, port = port)
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
'''