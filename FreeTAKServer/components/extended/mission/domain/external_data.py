from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class ExternalData(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)

        self.cot_attributes["mission"] = None
        self.cot_attributes["name"] = None
        self.cot_attributes["notes"] = None
        self.cot_attributes["tool"] = None
        self.cot_attributes["uid"] = None
        self.cot_attributes["urlData"] = None
        self.cot_attributes["urlView"] = None

    @CoTProperty
    def mission(self):
        return self.cot_attributes.get("mission", None)
    
    @mission.setter
    def mission(self, mission=None):
        self.cot_attributes["mission"] = mission
    
    @CoTProperty
    def name(self):
        return self.cot_attributes.get("name", None)
    
    @name.setter
    def name(self, name=None):
        self.cot_attributes["name"] = name
    
    @CoTProperty
    def notes(self):
        return self.cot_attributes.get("notes", None)
    
    @notes.setter
    def notes(self, notes=None):
        self.cot_attributes["notes"] = notes
    
    @CoTProperty
    def tool(self):
        return self.cot_attributes.get("tool", None)
    
    @tool.setter
    def tool(self, tool=None):
        self.cot_attributes["tool"] = tool
    
    @CoTProperty
    def uid(self):
        return self.cot_attributes.get("uid", None)
    
    @uid.setter
    def uid(self, uid=None):
        self.cot_attributes["uid"] = uid
    
    @CoTProperty
    def urlData(self):
        return self.cot_attributes.get("urlData", None)
    
    @urlData.setter
    def urlData(self, urlData=None):
        self.cot_attributes["urlData"] = urlData
    
    @CoTProperty
    def urlView(self):
        return self.cot_attributes.get("urlView", None)
    
    @urlView.setter
    def urlView(self, urlView=None):
        self.cot_attributes["urlView"] = urlView