from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class checklists(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)

    @CoTProperty
    def checklist(self):
        return self.__checklist

    @checklist.setter
    def checklist(self, checklist=None):
        self.__checklist = checklist