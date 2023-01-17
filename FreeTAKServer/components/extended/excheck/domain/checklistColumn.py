from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class checklistColumn(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(__class__.__name__, configuration, model)

    @CoTProperty
    def columnName(self):
        return self.__columnName

    @columnName.setter
    def columnName(self, columnName=None):
        self.__columnName = columnName

    @CoTProperty
    def columnType(self):
        return self.__columnType

    @columnType.setter
    def columnType(self, columnType=None):
        self.__columnType = columnType

    @CoTProperty
    def columnWidth(self):
        return self.__columnWidth

    @columnWidth.setter
    def columnWidth(self, columnWidth=None):
        self.__columnWidth = columnWidth