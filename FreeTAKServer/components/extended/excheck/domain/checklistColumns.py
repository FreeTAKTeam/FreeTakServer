from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class checklistColumns(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)

    @CoTProperty
    def checklistColumn(self):
        return self.__checklistColumn

    @checklistColumn.setter
    def checklistColumn(self, checklistColumn=None):
        self.__checklistColumn = checklistColumn
