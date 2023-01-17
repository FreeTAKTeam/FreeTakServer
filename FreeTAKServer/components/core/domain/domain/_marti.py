from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.Dest import Dest as DestObject
from digitalpy.core.parsing.load_configuration import Configuration
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


# TODO: modify to call dest with static method
class counter:
    count = 0
    getter_called = False


class marti(
    CoTNode
):  # ignore this because the class name must match that of the CoT ignore pylint: disable=invalid-name
    __counter = counter()

    def __init__(self, configuration: Configuration, model, registry=None):
        # self.__dest = [DestObject(self.__counter)]
        # self.__tempdest = self.__dest
        self.__index = 0
        # self.__firstrun = True
        super().__init__(self.__class__.__name__, configuration, model, registry, {})