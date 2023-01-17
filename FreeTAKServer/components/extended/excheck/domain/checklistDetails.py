from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class checklistDetails(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
    
    @CoTProperty
    def name(self):
        return self.__name

    @name.setter
    def name(self, name=None):
        self.__name = name

    @CoTProperty
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, uid=None):
        self.__uid = uid

    @CoTProperty
    def description(self):
        return self.__description

    @description.setter
    def description(self, description=None):
        self.__description = description

    @CoTProperty
    def startTime(self):
        return self.__startTime

    @startTime.setter
    def startTime(self, startTime=None):
        self.__startTime = startTime

    @CoTProperty
    def templateName(self):
        return self.__templateName

    @templateName.setter
    def templateName(self, templateName=None):
        self.__templateName = templateName

    @CoTProperty
    def creatorUid(self):
        return self.__creatorUid

    @creatorUid.setter
    def creatorUid(self, creatorUid=None):
        self.__creatorUid = creatorUid

    @CoTProperty
    def creatorCallsign(self):
        return self.__creatorCallsign

    @creatorCallsign.setter
    def creatorCallsign(self, creatorCallsign=None):
        self.__creatorCallsign = creatorCallsign
