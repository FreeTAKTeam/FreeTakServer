from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MissionExternalData
    from . import creatorUid

class MissionChange(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)

    @CoTProperty
    def contentResource(self):
        data = self.cot_attributes.get("contentResource", None)
        if data is None:
            raise AttributeError("attribute 'contentResource' doesnt exist")
        return data

    @contentResource.setter
    def contentResource(self, contentResource):
        self.cot_attributes["contentResource"] = contentResource

    @CoTProperty
    def externalData(self)->'MissionExternalData':
        data = self.cot_attributes.get("externalData", None)
        if data is None:
            raise AttributeError("attribute 'externalData' doesnt exist")
        return data
    
    @externalData.setter
    def externalData(self, externalData):
        self.cot_attributes["externalData"] = externalData

    @CoTProperty
    def isFederatedChange(self):
        data = self.cot_attributes.get("isFederatedChange", None)
        if data is None:
            raise AttributeError("attribute 'isFederatedChange' doesnt exist")
        return data

    @isFederatedChange.setter
    def isFederatedChange(self, isFederatedChange):
        self.cot_attributes["isFederatedChange"] = isFederatedChange
    
    @CoTProperty
    def groupVector(self):
        data = self.cot_attributes.get("groupVector", None)
        if data is None:
            raise AttributeError("attribute 'groupVector' doesnt exist")
        return data

    @groupVector.setter
    def groupVector(self, groupVector):
        self.cot_attributes["groupVector"] = groupVector

    @CoTProperty
    def creatorUid(self) -> 'creatorUid':
        data = self.cot_attributes.get("creatorUid", None)
        if data is None:
            raise AttributeError("attribute 'creatorUid' doesnt exist")
        return data

    @creatorUid.setter
    def creatorUid(self, creatorUid):
        self.cot_attributes["creatorUid"] = creatorUid

    @CoTProperty
    def missionName(self):
        data = self.cot_attributes.get("missionName", None)
        if data is None:
            raise AttributeError("attribute 'missionName' doesnt exist")
        return data

    @missionName.setter
    def missionName(self, missionName):
        self.cot_attributes["missionName"] = missionName

    @CoTProperty
    def timestamp(self):
        data = self.cot_attributes.get("timestamp", None)
        if data is None:
            raise AttributeError("attribute 'timestamp' doesnt exist")
        return data

    @timestamp.setter
    def timestamp(self, timestamp):
        self.cot_attributes["timestamp"] = timestamp

    @CoTProperty
    def type(self):
        data = self.cot_attributes.get("type", None)
        if data is None:
            raise AttributeError("attribute 'type' doesnt exist")
        return data

    @type.setter
    def type(self, type):
        self.cot_attributes["type"] = type

    @CoTProperty
    def content(self):
        data = self.cot_attributes.get("content", None)
        if data is None:
            raise AttributeError("attribute 'content' doesnt exist")
        return data

    @content.setter
    def content(self, content):
        self.cot_attributes["content"] = content

    @CoTProperty
    def details(self):
        data = self.cot_attributes.get("details", None)
        if data is None:
            raise AttributeError("attribute 'details' doesnt exist")
        return data
    
    @details.setter
    def details(self, details):
        self.cot_attributes["details"] = details

    @CoTProperty
    def contentUid(self):
        data = self.cot_attributes.get("contentUid", None)
        if data is None:
            raise AttributeError("attribute 'contentUid' doesnt exist")
        return data
    
    @contentUid.setter
    def contentUid(self, contentUid):
        self.cot_attributes["contentUid"] = contentUid