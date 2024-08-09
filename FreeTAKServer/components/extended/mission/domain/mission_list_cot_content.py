from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import ModelConfiguration

class MissionListCoTContent(CoTNode):
    def __init__(self, configuration: ModelConfiguration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["data"] = None
        self.cot_attributes["timestamp"] = None
        self.cot_attributes["creatorUid"] = None

    @CoTProperty
    def data(self):
        data = self.cot_attributes.get("data", None)
        if data is None:
            raise AttributeError("attribute 'data' doesnt exist")
        return data
    
    @data.setter
    def data(self, data):
        self.cot_attributes["data"] = data

    @CoTProperty
    def timestamp(self):
        data = self.cot_attributes.get("timestamp", None)
        if data is None:
            raise AttributeError("attribute 'timestamp' doesnt exist")
        return data
    
    @timestamp.setter
    def timestamp(self, timestamp):
        self.cot_attributes["timestamp"] = timestamp

    @CoTProperty
    def creatorUid(self):
        data = self.cot_attributes.get("creatorUid", None)
        if data is None:
            raise AttributeError("attribute 'creatorUid' doesnt exist")
        return data
    
    @creatorUid.setter
    def creatorUid(self, creatorUid):
        self.cot_attributes["creatorUid"] = creatorUid