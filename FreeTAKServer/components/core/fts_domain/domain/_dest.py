from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.DestVariables import DestVariables as vars
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import ModelConfiguration
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode


class dest(CoTNode):
    def __init__(self, configuration: ModelConfiguration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["callsign"] = None
        self.cot_attributes["mission"] = None

    @CoTProperty
    def callsign(self):
        return self.cot_attributes["callsign"]

    @callsign.setter
    def callsign(self, callsign: str):
        self.cot_attributes["callsign"] = callsign

    @CoTProperty
    def mission(self):
        return self.cot_attributes["mission"]
    
    @mission.setter
    def mission(self, mission: str):
        self.cot_attributes["mission"] = mission