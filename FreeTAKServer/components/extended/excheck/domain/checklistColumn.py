from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class checklistColumn(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(__class__.__name__, configuration, model)

    @CoTProperty
    def columnName(self):
        return self.cot_attributes.get("columnName", None)

    @columnName.setter
    def columnName(self, columnName=None):
        self.cot_attributes["columnName"] = columnName

    @CoTProperty
    def columnType(self):
        return self.cot_attributes.get("columnType", None)

    @columnType.setter
    def columnType(self, columnType=None):
        self.cot_attributes["columnType"] = columnType

    @CoTProperty
    def columnWidth(self):
        return self.cot_attributes.get("columnWidth", None)

    @columnWidth.setter
    def columnWidth(self, columnWidth=None):
        self.cot_attributes["columnWidth"] = columnWidth