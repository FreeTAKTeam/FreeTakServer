from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty
from digitalpy.core.parsing.load_configuration import Configuration

class location(CoTNode):
    def __init__(self, configuration: Configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["lat"] = None
        self.cot_attributes["lon"] = None

    @CoTProperty
    def lat(self):
        data = self.cot_attributes.get("lat", None)
        if data is None:
            raise AttributeError("attribute 'lat' doesnt exist")
        return data
    
    @lat.setter
    def lat(self, lat):
        self.cot_attributes["lat"] = lat

    @CoTProperty
    def lon(self):
        data = self.cot_attributes.get("lon", None)
        if data is None:
            raise AttributeError("attribute 'lon' doesnt exist")
        return data
    
    @lon.setter
    def lon(self, lon):
        self.cot_attributes["lon"] = lon
