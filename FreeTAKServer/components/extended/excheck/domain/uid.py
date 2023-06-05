from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.UidVariables import UidVariables as vars

class Uid(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["text"] = None
        self.cot_attributes["Droid"] = None

    @property
    def text(self):
        return self.cot_attributes.get("text", None)

    @text.setter
    def text(self, text):
        self.cot_attributes["text"] = text

    @CoTProperty
    def Droid(self):
        return self.cot_attributes.get("text", None)

    @Droid.setter
    def Droid(self, Droid = None):
        self.cot_attributes["Droid"] = Droid
