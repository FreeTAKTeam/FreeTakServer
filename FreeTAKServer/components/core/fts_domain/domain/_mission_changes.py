from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from . import MissionChange
class MissionChanges(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)

    @CoTProperty
    def MissionChange(self)-> List['MissionChange']:
        return self.get_children_ex(children_type="MissionChange")
    
    @MissionChange.setter
    def MissionChange(self, MissionChange):
        self.add_child(MissionChange)