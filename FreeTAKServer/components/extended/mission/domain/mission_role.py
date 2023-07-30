from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionRole(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["permissions"] = None
        self.cot_attributes["type"] = None

    @CoTProperty
    def permissions(self):
        return self.cot_attributes.get("permissions", None)
    
    @permissions.setter
    def permissions(self, permissions=None):
        self.cot_attributes["permissions"] = permissions
    
    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)
    
    @type.setter
    def type(self, type=None):
        self.cot_attributes["type"] = type