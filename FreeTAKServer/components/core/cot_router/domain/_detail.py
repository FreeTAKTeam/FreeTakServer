from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode


class detail(CoTNode):
    
    def __init__(self, configuration, model):
        self.cot_attributes = {}
        
        super().__init__(self.__class__.__name__, configuration, model)
        self.xml_string = None
        
    def get_xml_string(self):
        return self.xml_string
    
    def set_xml_string(self, xml_string):
        self.xml_string = xml_string