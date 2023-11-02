from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.UidVariables import UidVariables as vars

class urlData(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)

    @property
    def text(self):
        return self.cot_attributes.get("text", None)

    @text.setter
    def text(self, text):
        self.cot_attributes["text"] = text