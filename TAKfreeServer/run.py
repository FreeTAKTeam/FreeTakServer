
from server import startup
import httpServer
import constants
import threading
import queue
import os
import ascii
const = constants.vars()

tcpServerThread = threading.Thread(target = startup, args = (), daemon=True)
tcpServerThread.start()
httpServerThread= threading.Thread(target = httpServer.startup, args = (), daemon=True)
httpServerThread.start()

tcpServerThread.join()
httpServerThread.join()