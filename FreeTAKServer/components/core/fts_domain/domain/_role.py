from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from FreeTAKServer.components.extended.mission.domain import permissions

class role(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["type"] = None
        if self.cot_attributes.get('permissions', None) is None:
            self.cot_attributes["permissions"] = None
        
    @CoTProperty
    def permissions(self)->'permissions':
        return self.cot_attributes['permissions']
    
    @permissions.setter
    def permissions(self, permissions=None):
        self.cot_attributes["permissions"] = permissions
    
    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)
    
    @type.setter
    def type(self, type=None):
        self.cot_attributes["type"] = type