from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class checklistDetails(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
    
    @CoTProperty
    def name(self):
        return self.cot_attributes.get("name", None)

    @name.setter
    def name(self, name=None):
        self.cot_attributes["name"] = name

    @CoTProperty
    def uid(self):
        return self.cot_attributes.get("uid", None)

    @uid.setter
    def uid(self, uid=None):
        self.cot_attributes["uid"] = uid

    @CoTProperty
    def description(self):
        return self.cot_attributes.get("description", None)

    @description.setter
    def description(self, description=None):
        self.cot_attributes["description"] = description

    @CoTProperty
    def startTime(self):
        return self.cot_attributes.get("startTime", None)

    @startTime.setter
    def startTime(self, startTime=None):
        self.cot_attributes["startTime"] = startTime

    @CoTProperty
    def templateName(self):
        return self.cot_attributes.get("templateName", None)

    @templateName.setter
    def templateName(self, templateName=None):
        self.cot_attributes["templateName"] = templateName

    @CoTProperty
    def creatorUid(self):
        return self.cot_attributes.get("creatorUid", None)

    @creatorUid.setter
    def creatorUid(self, creatorUid=None):
        self.cot_attributes["creatorUid"] = creatorUid

    @CoTProperty
    def creatorCallsign(self):
        return self.cot_attributes.get("creatorCallsign", None)

    @creatorCallsign.setter
    def creatorCallsign(self, creatorCallsign=None):
        self.cot_attributes["creatorCallsign"] = creatorCallsign
