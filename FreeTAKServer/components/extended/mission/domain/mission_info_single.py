from typing import List
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from FreeTAKServer.components.extended.excheck.domain.mission_data import MissionData
from FreeTAKServer.components.extended.mission.domain.mission_log import MissionLog
from FreeTAKServer.components.extended.mission.domain.mission_subscription import MissionSubscription

class MissionInfoSingle(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["version"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["nodeId"] = None
        self.cot_attributes["data"] = None

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
    def data(self) -> MissionSubscription | MissionLog | MissionData | None:
        data_val: MissionSubscription | MissionLog | MissionData = self.cot_attributes.get("data", None)
        if data_val != None: # type: ignore
            return data_val
        
        mission_subscription: MissionSubscription = self.cot_attributes.get("MissionSubscription", None)
        if mission_subscription != None:
            return mission_subscription
        
        mission_log: MissionLog = self.cot_attributes.get("MissionLog", None)
        if mission_log != None:
            return mission_log
        
        mission_data: MissionData = self.cot_attributes.get("MissionData", None)
        if mission_data != None:
            return mission_data
        
    @data.setter
    def data(self, data: MissionData | MissionSubscription | MissionLog):
        if self.cot_attributes.get("data") != None:
            if isinstance(data, self.cot_attributes.get("data").__class__):
                self.cot_attributes["data"] = data
            else:
                raise Exception("data type mismatch")
        else:
            self.cot_attributes["data"] = data