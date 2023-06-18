from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionItem(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["filename"] = None
        self.cot_attributes["keywords"] = None
        self.cot_attributes["mimeType"] = None
        self.cot_attributes["name"] = None
        self.cot_attributes["submissionTime"] = None
        self.cot_attributes["submitter"] = None
        self.cot_attributes["uid"] = None
        self.cot_attributes["hash"] = None
        self.cot_attributes["size"] = None
        self.cot_attributes["tool"] = None
        self.cot_attributes["expiration"] = None

    @CoTProperty
    def filename(self):
        return self.cot_attributes.get("filename", None)
    
    @filename.setter
    def filename(self, filename=None):
        self.cot_attributes["filename"] = filename

    @CoTProperty
    def keywords(self):
        return self.cot_attributes.get("keywords", None)
    
    @keywords.setter
    def keywords(self, keywords=None):
        self.cot_attributes["keywords"] = keywords

    @CoTProperty
    def mimeType(self):
        return self.cot_attributes.get("mimeType", None)
    
    @mimeType.setter
    def mimeType(self, mimeType=None):
        self.cot_attributes["mimeType"] = mimeType

    @CoTProperty
    def name(self):
        return self.cot_attributes.get("name", None)
    
    @name.setter
    def name(self, name=None):
        self.cot_attributes["name"] = name

    @CoTProperty
    def submissionTime(self):
        return self.cot_attributes.get("submissionTime", None)
    
    @submissionTime.setter
    def submissionTime(self, submissionTime=None):
        self.cot_attributes["submissionTime"] = submissionTime

    @CoTProperty
    def submitter(self):
        return self.cot_attributes.get("submitter", None)
    
    @submitter.setter
    def submitter(self, submitter=None):
        self.cot_attributes["submitter"] = submitter

    @CoTProperty
    def uid(self):
        return self.cot_attributes.get("uid", None)
    
    @uid.setter
    def uid(self, uid=None):
        self.cot_attributes["uid"] = uid

    @CoTProperty
    def hash(self):
        return self.cot_attributes.get("hash", None)
    
    @hash.setter
    def hash(self, hash=None):
        self.cot_attributes["hash"] = hash

    @CoTProperty
    def size(self):
        return self.cot_attributes.get("size", None)
    
    @size.setter
    def size(self, size=None):
        self.cot_attributes["size"] = size

    @CoTProperty
    def tool(self):
        return self.cot_attributes.get("tool", None)
    
    @tool.setter
    def tool(self, tool=None):
        self.cot_attributes["tool"] = tool

    @CoTProperty
    def expiration(self):
        return self.cot_attributes.get("expiration", None)
    
    @expiration.setter
    def expiration(self, expiration=None):
        self.cot_attributes["expiration"] = expiration
