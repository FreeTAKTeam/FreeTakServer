r"""TAK server class.

Example:

>>>from TAKlib import TAK
>>>TAKSock = TAK("172.21.1.166", 8087)

OBS! Class is non-blocking
"""

# Imported modules
import socket
import sys
import time
import _thread

__all__ = ["TAK"]

# Tuneable parameters
DEBUGLEVEL = 0

# TAK Protocol defaults
TAK_PORT = 8087
TAK_HTTP_PORT = 8080
LOGPATH = "./logs/"

# TAK resource parameters (don't touch)
Clients = []
Threads = []

class TAK:

    """
    An instance of this class represents a TAK server.
    The instance is initially not connected; the start()
    method must be used to establish a connection.  Alternatively, the
    host name and optional port number can be passed to the
    constructor, too.
    """

    def __init__(self, host=None, port=0):
        """Constructor.
        When called without arguments, create an unstarted instance.
        With a hostname argument, it starts the instance; port number
        is optional.
        """
        self.debuglevel = DEBUGLEVEL
        self.logPath = LOGPATH
        self.Clients = Clients
        self.Threads = Threads
        self.host = host
        self.port = port
        self.shutdown = False
        self.errorLog = ""
        self.log = ""
        if host is not None:
            self.start(host, port)

    def start(self, host, port=0):
        """Start the server instance.
        The optional second argument is the port number, which
        defaults to the standard TAK port (8087).
        Don't try to start more than one instance.
        """

        try:
            if not port:
                port = TAK_PORT
            self.host = host
            self.port = port
            self.TAKSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.TAKSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.TAKSock.bind((host, port))
            self.TAKSock.listen(5)
            _thread.start_new_thread(self.listenForConnection,(self.TAKSock,))
            self.startHTTP(self.host, 8080)
            self.log = self.log + time.ctime(time.time()) + ' TAK Server started up on ' + str(host) + ' port ' + str(port) + '\n'
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " start() Error: " + str(e) + '\n'

    def startHTTP(self, host=None, port=0):
        """Start the http server instance.
        The optional second argument is the port number, which
        defaults to the standard TAK http port (8080).
        Don't try to start more than one instance.
        """
        try:
            if not port:
                port = TAK_HTTP_PORT
            self.httpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.httpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.httpSock.bind((host, port))
            self.httpSock.listen(5)
            _thread.start_new_thread(self.listenForConnection,(self.httpSock,))
            self.log = self.log + time.ctime(time.time()) + ' HTTP Server started up on ' + str(host) + ' port ' + str(port) + '\n'
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " startHTTP() Error: " + str(e) + '\n'

    def __del__(self):
        """Destructor -- close the connection."""
        if self.TAKSock:
            self.TAKSock.close()
        if self.httpSock:
            self.httpSock.close()

    def setDebugLevel(self, debuglevel):
        """Set the debug level.
        The higher it is, the more debug output you get (on sys.stdout).
        """
        self.debuglevel = debuglevel

    def getLog(self):
        """Returns standard error"""
        return self.log

    def getErrorLog(self):
        """Returns standard error"""
        return self.errorLog

    def close(self):
        """Stop the server."""
        try:
            TAKSock = self.TAKSock
            httpSock = self.httpSock
            self.TAKSock = None
            self.httpSock = None
            self.eof = True
            self.shutdown = True
            if TAKSock:
                TAKSock.close()
                self.log = self.log + time.ctime(time.time()) + ' TAK Server stopped'+ '\n'
            if httpSock:
                httpSock.close()
                self.log = self.log + time.ctime(time.time()) + ' HTTP Server stopped'+ '\n'
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " close() Error: " + str(e) + '\n'

    def sendTo(self, xmlData, host, port):
        """Send Data to specific Client, returns true on success"""
        try:
            conn = self.TAKSock.connect((host, port))
            conn.send(bytes(xmlData, 'utf-8'))
            conn.close()
            self.log = self.log + time.ctime(time.time()) + ' Sent Data to ' + str(host) + ':' + str(port) + '\n'
            return True
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " sendTo() Error: " + str(e) + '\n'
            return False, str(e)

    def sendToAll(self, xmlData):
        """Send Data to all connected Clients, returns true on success"""
        try:
            for client in self.Clients:
                conn = self.TAKSock.connect(client)
                self.TAKSock.send(bytes(xmlData, 'utf-8'))
                conn.close()
            self.log = self.log + time.ctime(time.time()) + ' Broadcast Data to all Clients' + '\n'
            return True
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " sendToAll() Error: " + str(e) + '\n'
            return False, str(e)

    def getTAKSocket(self):
        """Return the TAK socket object used internally."""
        return self.TAKSock

    def getHttpSocket(self):
        """Return the TAKhttp socket object used internally."""
        return self.httpSock

    def getThreads(self):
        """Return the thread IDs used internally."""
        return self.Threads

    def getClients(self):
        """Return the connected clients."""
        return self.Clients

    def TAKFileno(self):
        """Return the fileno() of the TAK socket object used internally."""
        return self.TAKSock.fileno()

    def httpFileno(self):
        """Return the fileno() of the TAKhttp socket object used internally."""
        return self.httpSock.fileno()

    def listenForConnection(self, socket):
        """Listen for connection and establish it"""
        try:
            while True:
                try:
                    conn, clientAddress = socket.accept()
                    if self.shutdown:
                        break
                    if conn.getsockname()[1] == 8087:
                        _thread.start_new_thread(self.newClient,(conn, clientAddress))
                        self.log = self.log + time.ctime(time.time()) + ' Connection from: ' + str(clientAddress) + 'on port' + str(conn.getsockname()[1]) + '\n'
                    elif conn.getsockname()[1] == 8080:
                        _thread.start_new_thread(self.newHTTP,(conn, clientAddress))
                except Exception as e:
                    self.errorLog = self.errorLog + time.ctime(time.time()) + " listenForConnection() Error: " + str(e) + '\n'
                    e = None
                    break
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " listenForConnection() Error: " + str(e) + '\n'
            e = None

    def newClient(self, conn, clientAddress):
        """Receive client data and broadcast to all connected clients"""
        try:
            self.Threads.append(_thread.get_ident())
            self.Clients.append(clientAddress)
            conn.settimeout(20)
            self.log = self.log + time.ctime(time.time()) + ' Started new thread: ' + str(_thread.get_ident()) + '\n'
            try:
                initialData = conn.recv(610)
                self.log = self.log + time.ctime(time.time()) + ' Received initial ' + str(len(initialData)) + ' bytes from: ' + str(clientAddress) + ' on thread: ' + str(_thread.get_ident()) + '\n'
                while True:
                    data = conn.recv(303)
                    self.log = self.log + time.ctime(time.time()) + ' Received ' + str(len(data)) + ' bytes from: ' + str(clientAddress) + ' on thread: ' + str(_thread.get_ident()) + '\n'
                    if len(data) < 1:
                        break
                    if self.shutdown:
                        break
                    for client in self.Clients:
                        conn.sendto(data, client)
                    self.log = self.log + time.ctime(time.time()) + ' Broadcast data from: ' + str(clientAddress) + ' to ' + str(len(self.Clients)) + ' clients on thread: ' + str(_thread.get_ident()) + '\n'
            finally:
                conn.close()
                self.Threads.remove(_thread.get_ident())
                self.log = self.log + time.ctime(time.time()) + ' Terminated thread: ' + str(_thread.get_ident()) + '\n'
                self.Clients.remove(clientAddress)
                self.log = self.log + time.ctime(time.time()) + ' Closed connection: ' + str(clientAddress) + '\n'
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " newClient() Error: " + str(e) + '\n'

    def newHTTP(self, conn, clientAdress):
        """Receive client http/1.1 GET requests and respond with 200 OK"""
        try:
            self.Threads.append(_thread.get_ident())
            conn.settimeout(20)
            try:
                while True:
                    data = conn.recv(303)
                    self.log = self.log + time.ctime(time.time()) + ' Received HTTP/1.1 GET request from: ' + str(clientAddress) + ' on thread: ' + str(_thread.get_ident()) + '\n'
                    if len(data) < 1:
                        break
                    if self.shutdown:
                        break
                    conn.send(bytes("HTTP/1.1 200 OK\r\n" +"Content-Type: text/xml\r\n"  +"\r\n" +"<html></html>\r\n", encoding='utf8'))
                    self.log = self.log + time.ctime(time.time()) + ' Responded with HTTP/1.1 200 OK to: ' + str(clientAddress) + ' on thread: ' + str(_thread.get_ident()) + '\n'
            except:
                conn.close()
            finally:
                conn.close()
                self.Threads.remove(_thread.get_ident())
        except Exception as e:
            self.errorLog = self.errorLog + time.ctime(time.time()) + " newHTTP() Error: " + e + '\n'
