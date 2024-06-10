from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import ModelConfiguration

class events(CoTNode):
    def __init__(self, configuration: ModelConfiguration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)