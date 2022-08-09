from digitalpy.model.node import Node

from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject

class contact(Node, FTSProtocolObject):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.callsign = None 
        self.endpoint = None
        self.iconsetpath = None
        self.uid = None
        self.name = None
        self.emailAddress = None
        self.xmppUsername = None
        self.sipAddress = None
        
    # iconsetpath getter 
    def geticonsetpath(self): 
        return self.iconsetpath 
 
    # iconsetpath setter 
    def seticonsetpath(self, iconsetpath=None):
        self.iconsetpath=iconsetpath 

    # sipAddress getter
    def getsipAddress(self):
        return self.sipAddress

    # sipAddress setter
    def setsipAddress(self, sipAddress=None):
        self.sipAddress=sipAddress

    # emailAddress setter
    def getemailAddress(self):
        return self.emailAddress

    # emailAddress getter
    def setemailAddress(self, emailAddress=None):
        self.emailAddress=emailAddress

    # emailAddress setter
    def getxmppUsername(self):
        return self.xmppUsername

    # emailAddress getter
    def setxmppUsername(self, xmppUsername=None):
        self.xmppUsername=xmppUsername

    # callsign getter 
    def getcallsign(self): 
        return self.callsign 
 
    # callsign setter 
    def setcallsign(self, callsign=None):
        self.callsign=callsign 
 
     
    # endpoint getter 
    def getendpoint(self): 
        return self.endpoint 
 
    # endpoint setter 
    def setendpoint(self, endpoint=None):
        self.endpoint=endpoint

    def getuid(self):
        return self.uid

        # uid setter 

    def setuid(self, uid=None):
        self.uid = uid 
        
    def getname(self):
        return self.name

        # name setter 

    def setname(self, name=None):
        self.name = name

    def getphone(self):
        return self.phone

    def setphone(self, phone=None):
        self.phone = phone