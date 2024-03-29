from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
#######################################################
# 
# usericon.py
# Python implementation of the Class usericon
# Generated by Enterprise Architect
# Created on(FTSProtocolObject):      11-Feb-2020 11(FTSProtocolObject):08(FTSProtocolObject):08 AM
# Original author: Corvo
# 
#######################################################
from FreeTAKServer.model.FTSModelVariables.UsericonVariables import UsericonVariables as vars
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

from digitalpy.core.parsing.load_configuration import Configuration

class usericon(CoTNode):
    def __init__(self, configuration: Configuration, model):
        
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["iconsetpath"] = None

        self.iconsetpath = None

    @CoTProperty
    def iconsetpath(self):
        return self.cot_attributes.get("iconsetpath", None)

    @iconsetpath.setter
    def iconsetpath(self, iconsetpath):
        self.cot_attributes["iconsetpath"] = iconsetpath
