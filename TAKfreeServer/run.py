from server import startup
import httpServer
import constants
import threading
import queue
const = constants.vars()
tcpServerThread = threading.Thread(target = startup, args = (), daemon=True)
tcpServerThread.start()
httpServerThread= threading.Thread(target = httpServer.startup(), args = (), daemon=True)
httpServerThread.start()