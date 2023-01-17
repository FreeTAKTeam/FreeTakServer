from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class checklist(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.__checklist = None

    @CoTProperty
    def checklistDetails(self):
        return self.__checklistDetails

    @checklistDetails.setter
    def checklistDetails(self, checklistDetails=None):
        self.__checklistDetails = checklistDetails

    @CoTProperty
    def checklistColumns(self):
        return self.__checklistColumns

    @checklistColumns.setter
    def checklistColumns(self, checklistColumns=None):
        self.__checklistColumns = checklistColumns

    @CoTProperty
    def checklistTasks(self):
        return self.__checklistTasks

    @checklistTasks.setter
    def checklistTasks(self, checklistTasks=None):
        self.__checklistTasks = checklistTasks

    

    
    

    
