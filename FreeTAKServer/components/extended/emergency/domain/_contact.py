from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode


class contact(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["callsign"] = None 
        self.cot_attributes["endpoint"] = None
        self.cot_attributes["iconsetpath"] = None
        self.cot_attributes["uid"] = None
        self.cot_attributes["name"] = None
        self.cot_attributes["emailAddress"] = None
        self.cot_attributes["xmppUsername"] = None
        self.cot_attributes["sipAddress"] = None
        
    # iconsetpath getter 
    def geticonsetpath(self): 
        return self.cot_attributes["iconsetpath"]
 
    # iconsetpath setter 
    def seticonsetpath(self, iconsetpath=None):
        self.cot_attributes["iconsetpath"]=iconsetpath 

    # sipAddress getter
    def getsipAddress(self):
        return self.cot_attributes["sipAddress"]

    # sipAddress setter
    def setsipAddress(self, sipAddress=None):
        self.cot_attributes["sipAddress"]=sipAddress

    # emailAddress setter
    def getemailAddress(self):
        return self.cot_attributes["emailAddress"]

    # emailAddress getter
    def setemailAddress(self, emailAddress=None):
        self.cot_attributes["emailAddress"]=emailAddress

    # emailAddress setter
    def getxmppUsername(self):
        return self.cot_attributes["xmppUsername"]

    # emailAddress getter
    def setxmppUsername(self, xmppUsername=None):
        self.cot_attributes["xmppUsername"]=xmppUsername

    # callsign getter 
    def getcallsign(self): 
        return self.cot_attributes["callsign"]
 
    # callsign setter 
    def setcallsign(self, callsign=None):
        self.cot_attributes["callsign"]=callsign 
 
     
    # endpoint getter 
    def getendpoint(self): 
        return self.cot_attributes["endpoint"]
 
    # endpoint setter 
    def setendpoint(self, endpoint=None):
        self.cot_attributes["endpoint"]=endpoint

    def getuid(self):
        return self.cot_attributes["uid"]

        # uid setter 

    def setuid(self, uid=None):
        self.uid = uid 
        
    def getname(self):
        return self.cot_attributes["name"]

        # name setter 

    def setname(self, name=None):
        self.name = name

    def getphone(self):
        return self.cot_attributes["phone"]

    def setphone(self, phone=None):
        self.phone = phone