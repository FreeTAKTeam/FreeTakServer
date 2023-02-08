import inspect
import uuid
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.object_id import ObjectId
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject



class CoTNode(Node, FTSProtocolObject):

    

    def __init__(self, node_type, configuration, model, registry, cot_attributes, oid=None):
        self.cot_attributes = {}
        self.text = ""
        oid = ObjectId(node_type, str(uuid.uuid4()))
        super().__init__(node_type=node_type, oid=oid, configuration=configuration, model=model, registry=registry, initial_data=self.cot_attributes)

    def get_properties(self):
        methods = inspect.getmembers(self.__class__)
        # iterate through the cot_attributes and for each, verify it is neither a none n'or a type value
        return [
            m[0]
            for m in methods
            if getattr(m[1], "is_cot", False)
            and self.cot_attributes.get(m[0], None) != None
            and not isinstance(self.cot_attributes.get(m[0], str), type)
        ]