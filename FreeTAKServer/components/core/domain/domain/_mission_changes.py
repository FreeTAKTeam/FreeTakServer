from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionChanges(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["MissionChange"] = []

    @CoTProperty
    def MissionChange(self):
        return self.get_children_ex(children_type="MissionChange")
    
    @MissionChange.setter
    def MissionChange(self, MissionChange):
        self.add_child(MissionChange)