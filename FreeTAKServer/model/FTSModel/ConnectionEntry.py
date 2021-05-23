from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.ConnectionEntryVariables import ConnectionEntryVariables as vars

class ConnectionEntry(FTSProtocolObject):
    def __init__(self):
        self.networkTimeout = None
        self.uid = None
        self.path = None
        self.protocol = None
        self.bufferTime = None
        self.address = None
        self.port = None
        self.roverPort = None
        self.rtspReliable = None
        self.ignoreEmbeddedKLV = None
        self.alias = None

    @staticmethod
    def VideoStream(NETWORKTIMEOUT=vars.VideoStream().networkTimeout, UID=vars.VideoStream().uid,
                    PATH=vars.VideoStream().path, PROTOCOL=vars.VideoStream().protocol,
                    BUFFERTIME=vars.VideoStream().bufferTime, ADDRESS=vars.VideoStream().address,
                    PORT=vars.VideoStream().port, ROVERPORT=vars.VideoStream().roverPort,
                    RTSPRELIABLE=vars.VideoStream().rtspReliable,
                    IGNOREEMBEDDEDKLV=vars.VideoStream().ignoreEmbeddedKLV, ALIAS=vars.VideoStream().alias, ):
        connectionentry = ConnectionEntry()
        connectionentry.setnetworkTimeout(NETWORKTIMEOUT)
        connectionentry.setuid(UID)
        connectionentry.setpath(PATH)
        connectionentry.setprotocol(PROTOCOL)
        connectionentry.setbufferTime(BUFFERTIME)
        connectionentry.setaddress(ADDRESS)
        connectionentry.setport(PORT)
        connectionentry.setroverPort(ROVERPORT)
        connectionentry.setrtspReliable(RTSPRELIABLE)
        connectionentry.setignoreEmbeddedKLV(IGNOREEMBEDDEDKLV)
        connectionentry.setalias(ALIAS)
        return connectionentry

    def getnetworkTimeout(self):
            return self.networkTimeout

    def setnetworkTimeout(self, networkTimeout):
        self.networkTimeout = networkTimeout

    def getuid(self):
            return self.uid

    def setuid(self, uid):
        self.uid = uid

    def getpath(self):
            return self.path

    def setpath(self, path):
        self.path = path

    def getprotocol(self):
            return self.protocol

    def setprotocol(self, protocol):
        self.protocol = protocol

    def getbufferTime(self):
            return self.bufferTime

    def setbufferTime(self, bufferTime):
        self.bufferTime = bufferTime

    def getaddress(self):
            return self.address

    def setaddress(self, address):
        self.address = address

    def getport(self):
            return self.port

    def setport(self, port):
        self.port = port

    def getroverPort(self):
            return self.roverPort

    def setroverPort(self, roverPort):
        self.roverPort = roverPort

    def getrtspReliable(self):
            return self.rtspReliable

    def setrtspReliable(self, rtspReliable):
        self.rtspReliable = rtspReliable

    def getignoreEmbeddedKLV(self):
            return self.ignoreEmbeddedKLV

    def setignoreEmbeddedKLV(self, ignoreEmbeddedKLV):
        self.ignoreEmbeddedKLV = ignoreEmbeddedKLV

    def getalias(self):
            return self.alias

    def setalias(self, alias):
        self.alias = alias