from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode


class columnName(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)