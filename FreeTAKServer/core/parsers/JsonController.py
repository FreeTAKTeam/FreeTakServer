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

    def serialize_emergency_post(self, json):
        """
        :arg json: the json to be serialized to an emergency
        """
        obj = EmergencyPost()
        return self.serialize_json_to_object(obj, json)

    def serialize_emergency_delete(self, json):
        object = EmergencyDelete()
        return self.serialize_json_to_object(object, json)

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