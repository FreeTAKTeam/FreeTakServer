from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class componentproperty(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["componentpropertyattribute"] = None

    @CoTProperty
    def componentpropertyattribute(self):
        return self.cot_attributes.get("componentpropertyattribute", None)

    @componentpropertyattribute.setter
    def componentpropertyattribute(self, componentpropertyattribute=None):
        self.cot_attributes["componentpropertyattribute"] = componentpropertyattribute

