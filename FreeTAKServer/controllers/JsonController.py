from FreeTAKServer.model.RestMessages.EmergencyPost import EmergencyPost
from FreeTAKServer.model.RestMessages.EmergencyDelete import EmergencyDelete
from FreeTAKServer.model.RestMessages.PresencePost import PresencePost
from FreeTAKServer.model.RestMessages.ChatPost import ChatPost
from FreeTAKServer.model.RestMessages.GeoObjectPost import GeoObjectPost

class JsonController:
    def __init__(self):
        pass

    def serialize_emergency_post(self, json):
        """
        :arg json: the json to be serialized to an emergency
        """
        object = EmergencyPost()
        return self.serialize_json_to_object(object, json)

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

    def serialize_json_to_object(self, object, json):
        for key in json.keys():
            s = dir(object)
            if key in dir(object):

                setter = getattr(object, 'set'+str(key))
                setter(json[key])

            else:
                raise Exception(f'attribute {key} not supported by this endpoint')

        return object