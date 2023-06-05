from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
import datetime as dt

class SubmissionTime(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["text"] = None

    @CoTProperty
    def text(self):
        return self.cot_attributes.get("text", None)

    @text.setter
    def text(self, text):
        self.cot_attributes["text"] = text

