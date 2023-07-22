from geopy import Nominatim
import uuid

from FreeTAKServer.model.RestMessages.EmergencyPost import EmergencyPost
from FreeTAKServer.model.RestMessages.EmergencyDelete import EmergencyDelete
from FreeTAKServer.model.RestMessages.PresencePost import PresencePost
from FreeTAKServer.model.RestMessages.ChatPost import ChatPost
from FreeTAKServer.model.RestMessages.GeoObjectPost import GeoObjectPost
from FreeTAKServer.model.RestMessages.RoutePost import RoutePost
from FreeTAKServer.model.RestMessages.DroneSensor import DroneSensor
from FreeTAKServer.model.RestMessages.SPISensor import SPISensor
from FreeTAKServer.model.RestMessages.ImageryVideo import ImageryVideo
from FreeTAKServer.model.RestMessages.VideoStreamDelete import VideoStreamDelete

class JsonController:
    def __init__(self):
        pass

    def resolve_address(self, json: dict, address_attrib: str="address"):
        if address_attrib in json:
            locator = Nominatim(user_agent=str(uuid.uuid4()))
            location = locator.geocode(json.get(address_attrib))
            return location.latitude, location.longitude
        else:
            return json.get("latitude", 0), json.get("longitude", 0)
        
    def serialize_emergency_post(self, json: dict):
        """expand the passed emergency_post values into a complete json description
        of the object
        
        json (dict): the json sent by the client
        """
        lat, lon = self.resolve_address(json)
        full_json = {
            "event": {
                "@uid": str(uuid.uuid4()),
                "@type": "EmergencyAlert",
                "@how": "h-e",
                "@time": None,   # these will be automatically created during object serialization
                "@start": None,  
                "@stale": None,
                "point": {
                    "@lat": lat,
                    "@lon": lon,
                    "@hae": "9999999",
                    "@ce": "9999999",
                    "@le": "9999999"
                },
                "detail": {
                    "remarks": {
                        "#text": str(json.get("remarks", ""))
                    },
                    "emergency": {
                        "@type": str(json.get("emergencyType")),
                        "#text": str(json.get("name"))
                    }
                }
            }
        }
        return full_json

    def serialize_emergency_delete(self, json):
        full_json = {
            "event": {
                "@how": "h-e",
                "@time": None,   # these will be automatically created during object serialization
                "@start": None,  
                "@stale": None,
                "@type": "EmergencyCancelled",
                "@uid": json.get("uid"),
                "@version": "2.0",
                "detail": {
                    "emergency": {
                    "@cancel": "true"
                    }
                },
                "point": {
                    "@ce": "9999999",
                    "@hae": "9999999",
                    "@lat": "0",
                    "@le": "9999999",
                    "@lon": "0"
                }
            }
        }

        return full_json

    def serialize_geoobject_post(self, json):
        object = GeoObjectPost()
        return self.serialize_json_to_object(object, json)

    def serialize_presence_post(self, json):
        object = PresencePost()
        return self.serialize_json_to_object(object, json)

    def serialize_chat_post(self, json):
        object = ChatPost()
        return self.serialize_json_to_object(object, json)
    
    def serialize_route_post(self, json):
        object = RoutePost()
        return self.serialize_json_to_object(object, json)

    def serialize_drone_sensor_post(self, json):
        object = DroneSensor()
        return self.serialize_json_to_object(object, json)

    def serialize_spi_post(self, json):
        object = SPISensor()
        return self.serialize_json_to_object(object, json)

    def serialize_imagery_video(self, json):
        object = ImageryVideo()
        return self.serialize_json_to_object(object, json)

    def serialize_video_stream_delete(self, json):
        object = VideoStreamDelete()
        return self.serialize_json_to_object(object, json)

    def serialize_json_to_object(self, obj, json):
        for key in json.keys():
            if key in dir(obj):
                setter = getattr(obj, 'set'+str(key))
                setter(json[key])

        return obj