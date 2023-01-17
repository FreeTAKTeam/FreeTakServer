from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class checklistTasks(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)

    @CoTProperty
    def checklistTask(self):
        return self.__checklistTask

    @checklistTask.setter
    def checklistTask(self, checklistTask=None):
        self.__checklistTask = checklistTask