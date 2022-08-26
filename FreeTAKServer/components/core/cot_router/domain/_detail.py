from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode


class detail(CoTNode):
    
    def __init__(self, configuration, model):
        self.cot_attributes = {}
        
        super().__init__(self.__class__.__name__, configuration, model)
        self._xml_string = None
        
    @property
    def xml_string(self):
        return self._xml_string
    
    @xml_string.setter
    def xml_string(self, xml_string):
        self._xml_string = xml_string