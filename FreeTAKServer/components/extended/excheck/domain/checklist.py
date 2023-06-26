from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class Checklist(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["checklist"] = None

    @CoTProperty
    def checklistDetails(self):
        return self.cot_attributes.get("checklistDetails", None)

    @checklistDetails.setter
    def checklistDetails(self, checklistDetails=None):
        self.cot_attributes["checklistDetails"] = checklistDetails

    @CoTProperty
    def checklistColumns(self):
        return self.cot_attributes.get("checklistColumns", None)

    @checklistColumns.setter
    def checklistColumns(self, checklistColumns=None):
        self.cot_attributes["checklistColumns"] = checklistColumns

    @CoTProperty
    def checklistTasks(self):
        return self.cot_attributes.get("checklistTasks", None)

    @checklistTasks.setter
    def checklistTasks(self, checklistTasks=None):
        self.cot_attributes["checklistTasks"] = checklistTasks

    

    
    

    
