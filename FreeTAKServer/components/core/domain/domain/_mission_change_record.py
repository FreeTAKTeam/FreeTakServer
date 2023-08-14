from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionChangeRecord(CoTNode):
    
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["type"] = None
        self.cot_attributes["contentUid"] = None
        self.cot_attributes["missionName"] = None
        self.cot_attributes["timestamp"] = None
        self.cot_attributes["creatorUid"] = None
        self.cot_attributes["serverTime"] = None
        self.cot_attributes["contentResource"] = None
        self.cot_attributes["detail"] = None

    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)
    
    @type.setter
    def type(self, type=None):
        self.cot_attributes["type"] = type

    @CoTProperty
    def contentUid(self):
        return self.cot_attributes.get("contentUid", None)
    
    @contentUid.setter
    def contentUid(self, contentUid=None):
        self.cot_attributes["contentUid"] = contentUid

    @CoTProperty
    def missionName(self):
        return self.cot_attributes.get("missionName", None)
    
    @missionName.setter
    def missionName(self, missionName=None):
        self.cot_attributes["missionName"] = missionName

    @CoTProperty
    def timestamp(self):
        return self.cot_attributes.get("timestamp", None)
    
    @timestamp.setter
    def timestamp(self, timestamp=None):
        self.cot_attributes["timestamp"] = timestamp

    @CoTProperty
    def creatorUid(self):
        return self.cot_attributes.get("creatorUid", None)
    
    @creatorUid.setter
    def creatorUid(self, creatorUid=None):
        self.cot_attributes["creatorUid"] = creatorUid

    @CoTProperty
    def serverTime(self):
        return self.cot_attributes.get("serverTime", None)
    
    @serverTime.setter
    def serverTime(self, serverTime=None):
        self.cot_attributes["serverTime"] = serverTime

    @CoTProperty
    def contentResource(self):
        return self.cot_attributes.get("contentResource", None)
    
    @contentResource.setter
    def contentResource(self, contentResource=None):
        self.cot_attributes["contentResource"] = contentResource

    @CoTProperty
    def detail(self):
        return self.cot_attributes.get("detail", None)
    
    @detail.setter
    def detail(self, detail=None):
        self.cot_attributes["detail"] = detail