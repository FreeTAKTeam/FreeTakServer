from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class TemplateMetaData(CoTNode):
    def __init__(self, configuration, model, oid=None):
        self.cot_attributes["timestamp"] = None
        self.cot_attributes["creatorUid"] = None

    @CoTProperty
    def timestamp(self):
        return self.get_children_ex(children_type="timestamp")

    @timestamp.setter
    def timestamp(self, timestamp):
        self.add_child(timestamp)

    @CoTProperty
    def creatorUid(self):
        return self.get_children_ex(children_type="creatorUid")

    @creatorUid.setter
    def creatorUid(self, creatorUid):
        self.add_child(creatorUid)