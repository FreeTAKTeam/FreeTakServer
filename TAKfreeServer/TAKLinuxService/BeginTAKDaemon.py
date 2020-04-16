
import sys
import os
import daemon
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from TAKfreeServer.server import ThreadedServer
if __name__ == "__main__":
	with daemon.DaemonContext():
		ThreadedServer('your ip',const.DEFAULTPORT).listen()