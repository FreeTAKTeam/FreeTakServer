import threading

import httpServer
import server

tcpServerThread = threading.Thread(target = server.startup, args = (), daemon=True)
tcpServerThread.start()
httpServerThread= threading.Thread(target = httpServer.startup, args = (), daemon=True)
httpServerThread.start()

tcpServerThread.join()
httpServerThread.join()
