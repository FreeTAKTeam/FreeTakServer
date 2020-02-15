import socketserver
import threading
import time
from queue import Queue

NUMBEROFTHREADS= 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_Connection = []
All_Address= []

class FreTakServer(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    #listen and accept connections from clients
# send data received from a lient to all the connected lcients but this one




    def handle(self):
        stripstring = "\n"
        All_Address.append(self.client_address)
    
        while 1:
            self.data = self.request.recv(1024)
            if not self.data:
                break
            self.data = self.data.strip()
       
            print(str(self.client_address[0]) + " wrote: ")
            print (self.data)
            self.request.send(self.data)

if __name__ == "__main__":
    HOST, PORT = "192.168.0.104", 8087

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), FreTakServer) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

