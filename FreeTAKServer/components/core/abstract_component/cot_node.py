from digitalpy.model.node import Node
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
import inspect

class CoTNode(Node, FTSProtocolObject):
    
    def __init__(self, node_type, configuration, model):
        self.cot_attributes = {}
        self.text = ""
        super().__init__(node_type, configuration, model)
    
    @classmethod
    def get_all_properties(cls):
        methods = inspect.getmembers(cls)
        return [m[0] for m in methods if getattr(m[1], 'is_cot', False)]
    
    def turbo(self):
        type_mappings = db.query("SELECT * FROM type_table")
        self.type_table = type_mappings
        
    def get_internal_type(self, type):
        if cache == True:
            if self.type_table.get(type, None) != None:
                return self.type_table[type]
        human_readable_type = db.query(f"SELECT * FROM type_table WHERE type=='{type}'")
        self.type_table[type] = human_readable_type
        return human_readable_type
        
    def add_child(self, child):
        if self.validate_child_addition(child):
            self._children[child.get_id()]=child
            self.cot_attributes[child.__class__.__name__] = child
            child.set_parent(self)
        else:
            raise TypeError('child must be an instance of Node')