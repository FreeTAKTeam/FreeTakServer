from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.DestVariables import DestVariables as vars
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import Configuration
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode


class dest(CoTNode):
    def __init__(self, configuration: Configuration, model, registry=None):
        attributes = {}
        attributes["callsign"] = None
        super().__init__(self.__class__.__name__, configuration, model, registry, attributes)

    @CoTProperty
    def callsign(self):
        return self.__callsign

    @callsign.setter
    def callsign(self, callsign: str):
        self.__callsign = callsign
