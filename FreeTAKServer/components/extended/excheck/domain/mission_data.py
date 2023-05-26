from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class MissionData(CoTNode):
    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["name"] = None
        self.cot_attributes["tool"] = None
        self.cot_attributes["keywords"] = None
        self.cot_attributes["creatorUid"] = None
        self.cot_attributes["createTime"] = None
        self.cot_attributes["groups"] = None
        self.cot_attributes["externalData"] = None
        self.cot_attributes["feeds"] = None
        self.cot_attributes["mapLayers"] = None
        self.cot_attributes["inviteOnly"] = None
        self.cot_attributes["expiration"] = None
        self.cot_attributes["uids"] = None
        self.cot_attributes["passwordProtected"] = None
        self.cot_attributes["contents"] = []

    @CoTProperty
    def name(self):
        return self.cot_attributes.get("name", None)
    
    @name.setter
    def name(self, name=None):
        self.cot_attributes["name"] = name
    
    @CoTProperty
    def tool(self):
        return self.cot_attributes.get("tool")

    @tool.setter
    def tool(self, tool=None):
        self.cot_attributes["tool"] = tool

    @CoTProperty
    def keywords(self):
        return self.cot_attributes.get("keywords")

    @keywords.setter
    def keywords(self, keywords=None):
        self.cot_attributes["keywords"] = keywords

    @CoTProperty
    def creatorUid(self):
        return self.cot_attributes.get("creatorUid")
    
    @creatorUid.setter
    def creatorUid(self, creatorUid=None):
        self.cot_attributes["creatorUid"] = creatorUid

    @CoTProperty
    def createTime(self):
        return self.cot_attributes.get("createTime")
    
    @createTime.setter
    def createTime(self, createTime=None):
        self.cot_attributes["createTime"] = createTime

    @CoTProperty
    def groups(self):
        return self.cot_attributes.get("groups")
    
    @groups.setter
    def groups(self, groups=None):
        self.cot_attributes["groups"] = groups

    @CoTProperty
    def externalData(self):
        return self.cot_attributes.get("externalData")
    
    @externalData.setter
    def externalData(self, externalData=None):
        self.cot_attributes["externalData"] = externalData

    @CoTProperty
    def feeds(self):
        return self.cot_attributes.get("feeds")
    
    @feeds.setter
    def feeds(self, feeds=None):
        self.cot_attributes["feeds"] = feeds

    @CoTProperty
    def mapLayers(self):
        return self.cot_attributes.get("mapLayers")
    
    @mapLayers.setter
    def mapLayers(self, mapLayers=None):
        self.cot_attributes["mapLayers"] = mapLayers

    @CoTProperty
    def inviteOnly(self):
        return self.cot_attributes.get("inviteOnly")
    
    @inviteOnly.setter
    def inviteOnly(self, inviteOnly=None):
        self.cot_attributes["inviteOnly"] = inviteOnly

    @CoTProperty
    def expiration(self):
        return self.cot_attributes.get("expiration")
    
    @expiration.setter
    def expiration(self, expiration=None):
        self.cot_attributes["expiration"] = expiration

    @CoTProperty
    def uids(self):
        return self.cot_attributes.get("uids")
    
    @uids.setter
    def uids(self, uids=None):
        self.cot_attributes["uids"] = uids

    @CoTProperty
    def passwordProtected(self):
        return self.cot_attributes.get("passwordProtected")
    
    @passwordProtected.setter
    def passwordProtected(self, passwordProtected=None):
        self.cot_attributes["passwordProtected"] = passwordProtected

    @CoTProperty
    def contents(self):
        return self.get_children_ex(children_type="TemplateMetaData")

    @contents.setter
    def contents(self, contents):
        self.add_child(contents)