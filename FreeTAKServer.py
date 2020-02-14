import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
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
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()