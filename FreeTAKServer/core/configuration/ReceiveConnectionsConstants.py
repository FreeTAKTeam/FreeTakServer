class ReceiveConnectionsConstants:
    def __init__(self):
        self.RECEIVECONNECTIONDATATIMEOUT = 30
        self.CONNECTION_DATA_BUFFER = 1024
        self.TESTDATA = 'TEST'
        # timeout for the wrap socket operation in seconds
        self.WRAP_SSL_TIMEOUT = 1.0
        # number of clients that can attempt to connect at once
        self.LISTEN_COUNT = 2000
        # ssl socket timeout
        self.SSL_SOCK_TIMEOUT = 60