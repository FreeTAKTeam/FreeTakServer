from abc import abstractmethod
from FreeTAKServer.model.SpecificCoT.SpecificCoTAbstract import SpecificCoTAbstract
from typing import NewType
from FreeTAKServer.controllers.serializers.json_serializer import JsonSerializer
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.RestMessages.GeoObject import RestEnumerations
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables
from FreeTAKServer.model.SpecificCoT.SendSimpleCoT import SendSimpleCoT
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.controllers.configuration.types import Types
from lxml import etree


class AbstractApiAdapter(JsonSerializer):
    __specificCoT = NewType("specificCoT", SpecificCoTAbstract)

    @abstractmethod
    def from_api_to_fts_object(self, apiJson: dict) -> __specificCoT:
        raise NotImplementedError

    def _create_cot_object(self, serialized_json: dict, expected_fts_obj: Event, final_cot_object: Types.specific_cot) -> Types.specific_cot:
        fts_object = super().from_format_to_fts_object(serialized_json, expected_fts_obj)
        CoTObject = final_cot_object
        CoTObject.setModelObject(fts_object)
        CoTObject.setXmlString(etree.tostring(XmlSerializer().from_fts_object_to_format(fts_object)))
        return CoTObject


class GeoObjectAdapter(AbstractApiAdapter):

    def from_api_to_fts_object(self, api_json: dict) -> Types.specific_cot:

        serialized_json = self.serialize_initial_json(api_json)
        CoTObject = self._create_cot_object(serialized_json, Event.SimpleCoT(), SendSimpleCoT())
        return CoTObject

    def serialize_initial_json(self, api_json: dict) -> dict:
        api_json['how'] = RestEnumerations.how[api_json['how']]
        if "-.-" in RestEnumerations.geoObject[api_json["geoObject"]]:
            api_json['type'] = RestEnumerations.geoObject[api_json["geoObject"]].replace("a-.-", RestEnumerations.attitude[api_json['attitude']])
        else:
            raise Exception('geoObject not supported')
        del(api_json['attitude'])
        del(api_json['geoObject'])
        api_json['lon'] = api_json['longitude']
        del(api_json['longitude'])
        api_json['lat'] = api_json['latitude']
        del(api_json['latitude'])
        api_json['callsign'] = api_json['name']
        del(api_json['name'])
        import datetime as dt
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        timer = dt.datetime
        now = timer.utcnow()
        zulu = now.strftime(DATETIME_FMT)
        if 'timeout' in api_json:
            add = dt.timedelta(seconds=int(api_json['timeout']))
            del (api_json['timeout'])
        else:
            import datetime as dt
            add = dt.timedelta(seconds=RestAPIVariables.defaultGeoObjectTimeout)
        stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
        api_json['stale'] = stale_part.strftime(DATETIME_FMT)
        return api_json


class ChatAdapter(AbstractApiAdapter):

    def from_api_to_fts_object(self, api_json: dict) -> Types.specific_cot:
        from FreeTAKServer.model.SpecificCoT.SendGeoChat import SendGeoChat
        serialized_json = self.serialize_initial_json(api_json)
        CoTObject = self._create_cot_object(serialized_json, Event.GeoChat(), SendGeoChat())
        return CoTObject

    def serialize_initial_json(self, api_json: dict) -> dict:
        api_json['source'] = api_json['sender']
        del(api_json['sender'])
        api_json['INTAG'] = api_json['message']
        api_json['link'] = {"uid": api_json['source']}
        del(api_json['message'])
        return api_json


class PresenceAdapter(AbstractApiAdapter):

    def from_api_to_fts_object(self, api_json: dict) -> Types.specific_cot:
        from FreeTAKServer.model.SpecificCoT.SendPrecense import SendPresence
        serialized_json = self.serialize_initial_json(api_json)
        CoTObject = self._create_cot_object(serialized_json, Event.Presence(), SendPresence())
        return CoTObject

    def serialize_initial_json(self, api_json: dict) -> dict:
        api_json['type'] = RestAPIVariables.defaultPresenceType
        api_json['lon'] = api_json['longitude']
        del (api_json['longitude'])
        api_json['lat'] = api_json['latitude']
        del (api_json['latitude'])
        api_json['callsign'] = api_json['name']
        del (api_json['name'])
        api_json['how'] = RestEnumerations.how[api_json['how']]
        api_json['role'] = RestEnumerations.roles[api_json['role']]
        api_json['_group'] = {"name": RestEnumerations.Teams[api_json["team"]]}
        del(api_json['team'])
        import datetime as dt
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        timer = dt.datetime
        now = timer.utcnow()
        zulu = now.strftime(DATETIME_FMT)
        if 'timeout' in api_json:
            add = dt.timedelta(seconds=int(api_json['timeout']))
            del (api_json['timeout'])
        else:
            import datetime as dt
            add = dt.timedelta(seconds=RestAPIVariables.defaultGeoObjectTimeout)
        stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
        api_json['stale'] = stale_part.strftime(DATETIME_FMT)
        return api_json


class EmergencyOnAdapter(AbstractApiAdapter):

    def from_api_to_fts_object(self, api_json: dict) -> Types.specific_cot:
        from FreeTAKServer.model.SpecificCoT.SendEmergency import SendEmergency
        serialized_json = self.serialize_initial_json(api_json)
        CoTObject = self._create_cot_object(serialized_json, Event.emergecyOn(), SendEmergency())
        return CoTObject

    def serialize_initial_json(self, api_json):
        if 'longitude' in api_json:
            api_json['lon'] = api_json['longitude']
            del (api_json['longitude'])
        if 'latitude' in 'lat':
            api_json['lat'] = api_json['latitude']
            del (api_json['latitude'])
        api_json['callsign'] = api_json['name']
        del(api_json['name'])
        api_json['event'] = {'type': RestEnumerations.emergencyTypes[api_json['emergencyType']]}
        api_json['emergency'] = {'type': api_json['emergencyType']}
        del(api_json['emergencyType'])
        return api_json


class EmergencyOffAdapter(AbstractApiAdapter):

    def from_api_to_fts_object(self, api_json: dict) -> Types.specific_cot:
        from FreeTAKServer.model.SpecificCoT.SendPrecense import SendPresence
        serialized_json = self.serialize_initial_json(api_json)
        CoTObject = self._create_cot_object(serialized_json, Event.Presence(), SendPresence())
        return CoTObject
