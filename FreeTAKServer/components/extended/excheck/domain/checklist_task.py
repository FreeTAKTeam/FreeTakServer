from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class ChecklistTasks(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)

    @CoTProperty
    def lineBreak(self):
        return self.cot_attributes.get("lineBreak", None)

    @lineBreak.setter
    def lineBreak(self, lineBreak=None):
        self.cot_attributes["lineBreak"] = lineBreak

    @CoTProperty
    def number(self):
        return self.cot_attributes.get("number", None)

    @number.setter
    def number(self, number=None):
        self.cot_attributes["number"] = number
    
    @CoTProperty
    def uid(self):
        return self.cot_attributes.get("uid", None)

    @uid.setter
    def uid(self, uid=None):
        self.cot_attributes["uid"] = uid

    @CoTProperty
    def value(self):
        return self.cot_attributes.get("value", None)

    @value.setter
    def value(self, value=None):
        self.cot_attributes["value"] = value

    @CoTProperty
    def status(self):
        return self.cot_attributes.get("status", None)

    @status.setter
    def status(self, status=None):
        self.cot_attributes["status"] = status

    @CoTProperty
    def CompleteDTG(self):
        return self.cot_attributes.get("CompleteDTG", None)

    @CompleteDTG.setter
    def CompleteDTG(self, CompleteDTG=None):
        self.cot_attributes["CompleteDTG"] = CompleteDTG
