from digitalpy.core.domain.node import Node
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
import inspect


class CoTNode(Node, FTSProtocolObject):
    def __init__(self, node_type, configuration, model):
        self.cot_attributes = {}
        self.text = ""
        super().__init__(node_type, configuration, model)

    def get_properties(self):
        methods = inspect.getmembers(self.__class__)
        return [
            m[0]
            for m in methods
            if getattr(m[1], "is_cot", False)
            and self.cot_attributes.get(m[0], None) != None
        ]

    def add_child(self, child):
        if self.validate_child_addition(child):
            self._children[child.get_oid().str_val] = child
            self.cot_attributes[child.__class__.__name__] = child
            child.set_parent(self)
        else:
            raise TypeError("child must be an instance of Node")
