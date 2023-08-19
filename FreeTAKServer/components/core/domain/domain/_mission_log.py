from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionLog(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["id"] = None
        self.cot_attributes["creatorUid"] = None
        self.cot_attributes["entryUid"] = None
        self.cot_attributes["missionNames"] = []
        self.cot_attributes["dtg"] = None
        self.cot_attributes["content"] = None
        self.cot_attributes["contentHashes"] = []
        self.cot_attributes["keywords"] = []
        self.cot_attributes["servertime"] = None
        self.cot_attributes["created"] = None

    @CoTProperty
    def creatorUid(self):
        return self.cot_attributes.get("creatorUid", None)

    @creatorUid.setter
    def creatorUid(self, creatorUid=None):
        self.cot_attributes["creatorUid"] = creatorUid

    @CoTProperty
    def entryUid(self):
        return self.cot_attributes.get("entryUid", None)

    @entryUid.setter
    def entryUid(self, entryUid=None):
        self.cot_attributes["entryUid"] = entryUid

    @CoTProperty
    def missionNames(self):
        return self.cot_attributes.get("missionNames", [])

    @missionNames.setter
    def missionNames(self, missionNames=None):
        self.cot_attributes["missionNames"] = missionNames

    @CoTProperty
    def dtg(self):
        return self.cot_attributes.get("dtg", None)

    @dtg.setter
    def dtg(self, dtg=None):
        self.cot_attributes["dtg"] = dtg

    @CoTProperty
    def contentHashes(self):
        return self.cot_attributes.get("contentHashes", [])

    @contentHashes.setter
    def contentHashes(self, contentHashes=None):
        self.cot_attributes["contentHashes"] = contentHashes

    @CoTProperty
    def keywords(self):
        return self.cot_attributes.get("keywords", [])

    @keywords.setter
    def keywords(self, keywords=None):
        self.cot_attributes["keywords"] = keywords

    @CoTProperty
    def servertime(self):
        return self.cot_attributes.get("servertime", None)
    
    @servertime.setter
    def servertime(self, servertime=None):
        self.cot_attributes["servertime"] = servertime
        
    @CoTProperty
    def created(self):
        return self.cot_attributes.get("created", None)
    
    @created.setter
    def created(self, created=None):
        self.cot_attributes["created"] = created
        
    @CoTProperty
    def id(self):
        return self.cot_attributes.get("id", None)
    
    @id.setter
    def id(self, id=None):
        self.cot_attributes["id"] = id

    @CoTProperty
    def content(self):
        return self.cot_attributes.get("content", None)
    
    @content.setter
    def content(self, content=None):
        self.cot_attributes["content"] = content