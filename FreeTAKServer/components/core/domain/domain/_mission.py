from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MissionChanges, role

class mission(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["name"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["tool"] = None
        self.cot_attributes["authorUid"] = None
        self.cot_attributes["token"] = None
        
    @CoTProperty
    def name(self):
        return self.cot_attributes.get("name", None)
    
    @name.setter
    def name(self, name=None):
        self.cot_attributes["name"] = name
    
    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)
    
    @type.setter
    def type(self, type=None):
        self.cot_attributes["type"] = type
    
    @CoTProperty
    def tool(self):
        return self.cot_attributes.get("tool", None)
    
    @tool.setter
    def tool(self, tool=None):
        self.cot_attributes["tool"] = tool
    
    @CoTProperty
    def authorUid(self):
        return self.cot_attributes.get("authorUid", None)
    
    @authorUid.setter
    def authorUid(self, authorUid=None):
        self.cot_attributes["authorUid"] = authorUid

    @CoTProperty
    def MissionChanges(self, MissionChanges=None) -> 'MissionChanges':
        return self.cot_attributes.get("MissionChanges", None)
    
    @MissionChanges.setter
    def MissionChanges(self, MissionChanges=None):
        self.cot_attributes["MissionChanges"] = MissionChanges

    @CoTProperty
    def role(self, role=None) -> 'role':
        return self.cot_attributes.get("role", None)
    
    @role.setter
    def role(self, role=None):
        self.cot_attributes["role"] = role

    @CoTProperty
    def token(self):
        return self.cot_attributes.get("token", None)
    
    @token.setter
    def token(self, token=None):
        self.cot_attributes["token"] = token
