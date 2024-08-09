from typing import TYPE_CHECKING, List

from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.Dest import Dest as DestObject
from digitalpy.core.parsing.load_configuration import ModelConfiguration
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

if TYPE_CHECKING:
    from . import dest

# TODO: modify to call dest with static method
class counter:
    count = 0
    getter_called = False


class marti(
    CoTNode
):  # ignore this because the class name must match that of the CoT ignore pylint: disable=invalid-name
    __counter = counter()

    def __init__(self, configuration: ModelConfiguration, model, oid=None):
        # self.__dest = [DestObject(self.__counter)]
        # self.__tempdest = self.__dest
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["dest"] = []
        self.__index = 0
        # self.__firstrun = True

    @CoTProperty
    def dest(self) -> List['dest']:
        return self.get_children_ex(children_type="dest")

    @dest.setter
    def dest(self, dest):
        self.add_child(dest)
