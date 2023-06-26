from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import Configuration
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode

class mission(CoTNode):
    def __init__(self, configuration: Configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["type"] = None
        self.cot_attributes["tool"] = None
        self.cot_attributes["name"] = None
        self.cot_attributes["authorUid"] = None

    @CoTProperty
    def MissionChanges(self):
        return self.cot_attributes["MissionChanges"]
    
    @MissionChanges.setter
    def MissionChanges(self, missionchanges):
        self.cot_attributes["MissionChanges"] = missionchanges

    @CoTProperty
    def type(self):
        return self.cot_attributes["type"]

    @type.setter
    def type(self, type):
        self.cot_attributes["type"] = type

    @CoTProperty
    def tool(self):
        return self.cot_attributes["tool"]
    
    @tool.setter
    def tool(self, tool):
        self.cot_attributes["tool"] = tool

    @CoTProperty
    def name(self):
        return self.cot_attributes["name"]

    @name.setter
    def name(self, name):
        self.cot_attributes["name"] = name
        
    @CoTProperty
    def authorUid(self):
        return self.cot_attributes["authorUid"]

    @authorUid.setter
    def authorUid(self, authorUid):
        self.cot_attributes["authorUid"] = authorUid
