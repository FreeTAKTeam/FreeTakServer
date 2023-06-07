from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class contentResource(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        
    @CoTProperty
    def filename(self):
        data = self.cot_attributes.get("filename", None)
        if data is None:
            raise AttributeError("attribute 'filename' doesnt exist")
        return data

    @filename.setter
    def filename(self, filename):
        self.cot_attributes["filename"] = filename

    @CoTProperty
    def hash(self):
        data = self.cot_attributes.get("hash", None)
        if data is None:
            raise AttributeError("attribute 'hash' doesnt exist")
        return data

    @hash.setter
    def hash(self, hash):
        self.cot_attributes["hash"] = hash

    @CoTProperty
    def keywords(self):
        data = self.cot_attributes.get("keywords", None)
        if data is None:
            raise AttributeError("attribute 'keywords' doesnt exist")
        return data

    @keywords.setter
    def keywords(self, keywords):
        self.cot_attributes["keywords"] = keywords

    @CoTProperty
    def mimeType(self):
        data = self.cot_attributes.get("mimeType", None)
        if data is None:
            raise AttributeError("attribute 'mimeType' doesnt exist")
        return data

    @mimeType.setter
    def mimeType(self, mimeType):
        self.cot_attributes["mimeType"] = mimeType

    @CoTProperty
    def name(self):
        data = self.cot_attributes.get("name", None)
        if data is None:
            raise AttributeError("attribute 'name' doesnt exist")
        return data

    @name.setter
    def name(self, name):
        self.cot_attributes["name"] = name

    @CoTProperty
    def size(self):
        data = self.cot_attributes.get("size", None)
        if data is None:
            raise AttributeError("attribute 'size' doesnt exist")
        return data

    @size.setter
    def size(self, size):
        self.cot_attributes["size"] = size

    @CoTProperty
    def submissionTime(self):
        data = self.cot_attributes.get("submissionTime", None)
        if data is None:
            raise AttributeError("attribute 'submissionTime' doesnt exist")
        return data

    @submissionTime.setter
    def submissionTime(self, submissionTime):
        self.cot_attributes["submissionTime"] = submissionTime

    @CoTProperty
    def submitter(self):
        data = self.cot_attributes.get("submitter", None)
        if data is None:
            raise AttributeError("attribute 'submitter' doesnt exist")
        return data

    @submitter.setter
    def submitter(self, submitter):
        self.cot_attributes["submitter"] = submitter

    @CoTProperty
    def tool(self):
        data = self.cot_attributes.get("tool", None)
        if data is None:
            raise AttributeError("attribute 'tool' doesnt exist")
        return data

    @tool.setter
    def tool(self, tool):
        self.cot_attributes["tool"] = tool

    @CoTProperty
    def uid(self):
        data = self.cot_attributes.get("uid", None)
        if data is None:
            raise AttributeError("attribute 'uid' doesnt exist")
        return data

    @uid.setter
    def uid(self, uid):
        self.cot_attributes["uid"] = uid