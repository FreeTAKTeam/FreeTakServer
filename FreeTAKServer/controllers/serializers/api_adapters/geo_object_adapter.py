from FreeTAKServer.controllers.serializers.api_adapters.api_adapters import AbstractApiAdapter, SpecificCoTAbstract
from typing import NewType
from FreeTAKServer.controllers.serializers.json_serializer import JsonSerializer
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.RestMessages.GeoObject import GeoObject, RestEnumerations
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables
from FreeTAKServer.model.SpecificCoT.SendSimpleCoT import SendSimpleCoT
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.controllers.configuration.types import Types
from lxml import etree


class GeoObjectAdapter(AbstractApiAdapter, JsonSerializer):

    def from_api_to_fts_object(self, api_json: dict) -> Types.specific_cot:

        serialized_json = self.serialize_initial_json(api_json)
        CoTObject = self.create_cot_object(serialized_json, Event.SimpleCoT(), SendSimpleCoT())
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
        else:
            import datetime as dt
            add = dt.timedelta(seconds=RestAPIVariables.defaultGeoObjectTimeout)
        stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
        api_json['stale'] = stale_part.strftime(DATETIME_FMT)
        del(api_json['timeout'])
        return api_json

    def create_cot_object(self, serialized_json: dict, expected_fts_obj: Event, final_cot_object: Types.specific_cot) -> Types.specific_cot:
        fts_object = super().from_format_to_fts_object(serialized_json, expected_fts_obj)
        CoTObject = final_cot_object
        CoTObject.setModelObject(fts_object)
        CoTObject.setXmlString(etree.tostring(XmlSerializer().from_fts_object_to_format(fts_object)))
        return CoTObject
