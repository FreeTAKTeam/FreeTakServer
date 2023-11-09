from typing import List
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.UidVariables import UidVariables as vars
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Permission

class Permissions(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        
    @CoTProperty
    def permission(self)-> List['Permission']:
        return self.get_children_ex(children_type="Permission")
    
    @permission.setter
    def MissionChange(self, permission):
        self.add_child(permission)