import time
import random
from pathlib import Path
from SMWinservice import SMWinservice
import os.path
import threading
import sys
import os
import argparse
import logging
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import server
import httpser
class PythonCornerExample(SMWinservice):
    _svc_name_ = "FTS main service"
    _svc_display_name_ = "FTS main service"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        tcpserver = threading.Thread(target = server.startup, args = (), daemon=True)
        tcpserver.start()
        app.run(host="0.0.0.0", port=8080)
        while self.isrunning:
            pass
        sys.exit()

if __name__ == '__main__':
    PythonCornerExample.parse_command_line()