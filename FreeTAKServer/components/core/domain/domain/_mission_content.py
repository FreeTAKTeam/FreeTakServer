from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from ._mission_content_data import MissionContentData

class MissionContent(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["timestamp"] = None
        self.cot_attributes["creatorUid"] = None
        self.cot_attributes["data"] = None

    @CoTProperty
    def timestamp(self):
        return self.cot_attributes.get("timestamp", None)
    
    @timestamp.setter
    def timestamp(self, timestamp=None):
        self.cot_attributes["timestamp"] = timestamp

    @CoTProperty
    def creatorUid(self):
        return self.cot_attributes.get("creatorUid", None)
    
    @creatorUid.setter
    def creatorUid(self, creatorUid=None):
        self.cot_attributes["creatorUid"] = creatorUid

    @CoTProperty
    def data(self) -> MissionContentData:
        return self.cot_attributes.get("MissionContentData") # type: ignore
    
    @data.setter
    def data(self, data=None):
        self.cot_attributes["MissionContentData"] = data