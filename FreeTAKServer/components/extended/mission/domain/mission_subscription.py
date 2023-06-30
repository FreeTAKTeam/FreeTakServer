from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionSubscription(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["token"] = None
        self.cot_attributes["clientUid"] = None
        self.cot_attributes["username"] = None
        self.cot_attributes["createTime"] = None
    
    @CoTProperty
    def token(self):
        return self.cot_attributes.get("token", None)
    
    @token.setter
    def token(self, token=None):
        self.cot_attributes["token"] = token
    
    @CoTProperty
    def clientUid(self):
        return self.cot_attributes.get("clientUid", None)
    
    @clientUid.setter
    def clientUid(self, clientUid=None):
        self.cot_attributes["clientUid"] = clientUid
    
    @CoTProperty
    def username(self):
        return self.cot_attributes.get("username", None)
    
    @username.setter
    def username(self, username=None):
        self.cot_attributes["username"] = username
    
    @CoTProperty
    def createTime(self):
        return self.cot_attributes.get("createTime", None)
    
    @createTime.setter
    def createTime(self, createTime=None):
        self.cot_attributes["createTime"] = createTime