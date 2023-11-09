from typing import List
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from ._mission_invitation import MissionInvitation
from digitalpy.core.parsing.load_configuration import Configuration

class MissionInvitationList(CoTNode):
    def __init__(self, configuration: Configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["version"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["nodeId"] = None
        
    @CoTProperty
    def data(self) -> List[MissionInvitation]:
        return self.get_children_ex("MissionInvitation")

    @data.setter
    def data(self, value: MissionInvitation):
        self.add_child(value)

    @CoTProperty
    def version(self):
        return self.cot_attributes["version"]
    
    @version.setter
    def version(self, value):
        self.cot_attributes["version"] = value

    @CoTProperty
    def type(self):
        return self.cot_attributes["type"]
    
    @type.setter
    def type(self, value):
        self.cot_attributes["type"] = value

    @CoTProperty
    def nodeId(self):
        return self.cot_attributes["nodeId"]
    
    @nodeId.setter
    def nodeId(self, value):
        self.cot_attributes["nodeId"] = value