from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from lxml import etree

class content(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["text"] = None

    @property
    def text(self):
        return self.cot_attributes.get("text", None)

    # TODO, change this to use proper sub-object
    @text.setter
    def text(self, text):
        if text != "":
            self.xml.append(etree.fromstring(text))