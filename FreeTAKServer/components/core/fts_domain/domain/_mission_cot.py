from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionCOT(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["type"] = None
        self.cot_attributes["callsign"] = None

    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)
    
    @type.setter
    def type(self, type=None):
        self.cot_attributes["type"] = type

    @CoTProperty
    def callsign(self):
        return self.cot_attributes.get("callsign", None)
    
    @callsign.setter
    def callsign(self, callsign=None):
        self.cot_attributes["callsign"] = callsign
