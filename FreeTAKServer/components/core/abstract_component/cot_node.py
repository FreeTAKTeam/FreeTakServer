import copy
from digitalpy.core.domain.node import Node
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
import inspect
from lxml import etree


class CoTNode(Node, FTSProtocolObject):
    def __init__(self, node_type, configuration, model, oid=None):
        # a dictionary containing the attributes of all cots
        self.cot_attributes = {}
        # an xml object containing the contents of a given CoT without corresponding domain definition
        self.xml = etree.Element(self.__class__.__name__)
        self.text = ""
        super().__init__(node_type, configuration, model, oid)

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

    def __getstate__(self):
        state = self.__dict__
        state_cp =  copy.copy(state)
        state_cp["xml"] = etree.tostring(self.xml)
        return state_cp

    def __setstate__(self, state):
        state["xml"] = etree.fromstring(state["xml"])
        self.__dict__ = state