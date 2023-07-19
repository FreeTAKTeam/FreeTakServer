from typing import List
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from FreeTAKServer.components.extended.excheck.domain.mission_data import MissionData
from FreeTAKServer.components.extended.mission.domain.mission_subscription import MissionSubscription

class MissionInfo(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["version"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["nodeId"] = None
        self.cot_attributes["data"] = []

    @CoTProperty
    def version(self):
        return self.cot_attributes.get("version", None)
    
    @version.setter
    def version(self, version=None):
        self.cot_attributes["version"] = version

    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)
    
    @type.setter
    def type(self, type=None):
        self.cot_attributes["type"] = type

    @CoTProperty
    def nodeId(self):
        return self.cot_attributes.get("nodeId", None)
    
    @nodeId.setter
    def nodeId(self, nodeId=None):
        self.cot_attributes["nodeId"] = nodeId

    @CoTProperty
    def data(self) -> List[MissionData | MissionSubscription]:
        children: List[MissionData] = self.get_children_ex(children_type="MissionData")
        children.extend(self.get_children_ex(children_type="MissionSubscription"))
        return children
    
    @data.setter
    def data(self, data: MissionData | MissionSubscription):
        self.add_child(data)