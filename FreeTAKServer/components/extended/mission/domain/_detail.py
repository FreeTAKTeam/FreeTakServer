from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import Configuration

class detail(CoTNode):
    def __init__(self, configuration: Configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["callsign"] = None
        self.cot_attributes["type"] = None

    @CoTProperty
    def callsign(self):
        data = self.cot_attributes.get("callsign", None)
        if data is None:
            raise AttributeError("attribute 'callsign' doesnt exist")
        return data
    
    @callsign.setter
    def callsign(self, callsign):
        self.cot_attributes["callsign"] = callsign

    @CoTProperty
    def type(self):
        data = self.cot_attributes.get("type", None)
        if data is None:
            raise AttributeError("attribute 'type' doesnt exist")
        return data
    
    @type.setter
    def type(self, type):
        self.cot_attributes["type"] = type