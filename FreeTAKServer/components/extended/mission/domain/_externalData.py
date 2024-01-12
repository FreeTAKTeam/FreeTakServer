from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import ModelConfiguration

class externalData(CoTNode):
    def __init__(self, configuration: ModelConfiguration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)

    
    @CoTProperty
    def name(self) -> str:
        return self.cot_attributes.get("name", None)
    
    @name.setter
    def name(self, name: str=None): # type: ignore
        self.cot_attributes["name"] = name
    
    @CoTProperty
    def notes(self) -> str:
        return self.cot_attributes.get("notes", None)
    
    @notes.setter
    def notes(self, notes: str=None): # type: ignore
        self.cot_attributes["notes"] = notes
    
    @CoTProperty
    def tool(self) -> str:
        return self.cot_attributes.get("tool", None)
    
    @tool.setter
    def tool(self, tool: str=None): # type: ignore
        self.cot_attributes["tool"] = tool
    
    @CoTProperty
    def uid(self) -> str:
        return self.cot_attributes.get("uid", None)
    
    @uid.setter
    def uid(self, uid: str=None): # type: ignore
        self.cot_attributes["uid"] = uid
    
    @CoTProperty
    def urlData(self) -> str:
        return self.cot_attributes.get("urlData", None)
    
    @urlData.setter
    def urlData(self, urlData: str=None): # type: ignore
        self.cot_attributes["urlData"] = urlData
    
    @CoTProperty
    def urlView(self) -> str:
        return self.cot_attributes.get("urlView", None)
    
    @urlView.setter
    def urlView(self, urlView: str=None): # type: ignore
        self.cot_attributes["urlView"] = urlView