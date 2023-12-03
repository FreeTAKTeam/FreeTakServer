from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from FreeTAKServer.components.core.domain.domain._role import role
from digitalpy.core.parsing.load_configuration import Configuration

class MissionInvitation(CoTNode):
    def __init__(self, configuration: Configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["missionName"] = None
        self.cot_attributes["invitee"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["creatorUid"] = None
        self.cot_attributes["createTime"] = None
        self.cot_attributes["token"] = None
        self.cot_attributes["role"] = None
        
    @CoTProperty
    def role(self) -> role:
        return self.cot_attributes.get("role", None)
    
    @role.setter
    def role(self, role=None):
        self.cot_attributes["role"] = role

    @CoTProperty
    def missionName(self):
        return self.cot_attributes.get("missionName", None)
    
    @missionName.setter
    def missionName(self, missionName=None):
        self.cot_attributes["missionName"] = missionName

    @CoTProperty
    def invitee(self):
        return self.cot_attributes.get("invitee", None)
    
    @invitee.setter
    def invitee(self, invitee=None):
        self.cot_attributes["invitee"] = invitee

    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)
    
    @type.setter
    def type(self, type=None):
        self.cot_attributes["type"] = type

    @CoTProperty
    def creatorUid(self):
        return self.cot_attributes.get("creatorUid", None)
    
    @creatorUid.setter
    def creatorUid(self, creatorUid=None):
        self.cot_attributes["creatorUid"] = creatorUid

    @CoTProperty
    def createTime(self):
        return self.cot_attributes.get("createTime", None)
    
    @createTime.setter
    def createTime(self, createTime=None):
        self.cot_attributes["createTime"] = createTime

    @CoTProperty
    def token(self):
        return self.cot_attributes.get("token", None)
    
    @token.setter
    def token(self, token=None):
        self.cot_attributes["token"] = token