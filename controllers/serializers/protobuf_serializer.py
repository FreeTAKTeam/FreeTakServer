from typing import List
from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent
from FreeTAKServer.controllers.serializers.serializer_abstract import SerializerAbstract
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer


class ProtobufSerializer(SerializerAbstract):
    def __init__(self):
        self.attribute_name_mapping = {'coordSource': 'how', 'ploc': '', 'palt': '', 'sendTime': 'time',
                                       'startTime': 'start', 'staleTime': 'stale', 'groupName': '', 'groupRole': '',
                                       'screenName': '', 'phone': '', 'binary': '', 'ptpUids': '',
                                       'battery': '', 'speed': '', 'course': '', 'ptpCallsigns': ''}

    def from_format_to_fts_object(self, object: type, FTSObject: Event) -> Event:
        for descriptor in object.event.DESCRIPTOR.fields:
            attribute_name = descriptor.name

            if attribute_name in self.attribute_name_mapping:
                attribute_name = self.attribute_name_mapping[attribute_name]

            if hasattr(FTSObject.detail, 'marti'):
                from FreeTAKServer.model.FTSModel.Dest import Dest

                for callsign in object.event.ptpCallsigns:
                    newdest = Dest()
                    newdest.setcallsign(callsign)
                    FTSObject.detail.marti.setdest(newdest)

            elif attribute_name != 'other' and attribute_name != '':

                setters = self._get_fts_object_var_setter(FTSObject, attribute_name)
                setter = self._get_method_in_method_list(setters, 'event')

                if attribute_name == 'time' or attribute_name == 'start' or attribute_name == 'stale':
                    import datetime
                    attribute = getattr(object.event, descriptor.name)
                    try:
                        setter(datetime.datetime.strftime(
                            datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(float(attribute) / 1000.0)),
                                                       "%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%dT%H:%M:%S.%fZ"))
                        continue
                    except:
                        setter(datetime.datetime.strftime(
                            datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(float(attribute) / 1000.0)),
                                                       "%Y-%m-%d %H:%M:%S"), "%Y-%m-%dT%H:%M:%S.%fZ"))
                        continue
                else:
                    setter(getattr(object.event, descriptor.name))

            elif attribute_name == 'other' and object.event.other != '':
                from lxml import etree
                xmldetail = etree.fromstring(object.event.other)
                xmldetail.remove(xmldetail.find('_flow-tags_'))

                if xmldetail.find('remarks'):
                    XmlSerializer().from_format_to_fts_object(etree.tostring(xmldetail).decode(), FTSObject)
                else:
                    xmldetail.append(etree.Element('remarks'))
                    xmldetail.find('remarks').text = 'From federation '
                    XmlSerializer().from_format_to_fts_object(etree.tostring(xmldetail).decode(), FTSObject)

        return FTSObject

    def from_fts_object_to_format(self, FTSObject: Event) -> type:
        try:
            obj = FederatedEvent()
            if hasattr(FTSObject.detail, 'marti'):
                for dest in FTSObject.detail.marti.dest:
                    callsign = dest.getcallsign()
                    if callsign:
                        obj.event.ptpCallsigns.append(callsign)
                    else:
                        pass

            for descriptor in obj.event.DESCRIPTOR.fields:
                attribute_name = descriptor.name

                if attribute_name in self.attribute_name_mapping:
                    attribute_name = self.attribute_name_mapping[attribute_name]

                if attribute_name != 'other' and attribute_name:
                    getters = self._get_fts_object_var_getter(FTSObject, attribute_name)
                    getter = self._get_method_in_method_list(getters, 'event')

                    if attribute_name == 'time' or attribute_name == 'start' or attribute_name == 'stale':
                        import datetime
                        attribute = getter()
                        setattr(obj.event, descriptor.name,
                                int(datetime.datetime.strptime(attribute, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000))
                    elif attribute_name in ['lat', 'lon', 'hae', 'ce', 'le', 'speed', 'course']:
                        setattr(obj.event, descriptor.name, float(getter()))
                    elif attribute_name == 'battery':
                        setattr(obj.event, descriptor.name, int(getter()))
                    else:
                        setattr(obj.event, descriptor.name, getter())

                else:
                    from lxml import etree
                    xmldetail = etree.tostring(XmlSerializer().from_fts_object_to_format(FTSObject.detail)).decode()
                    setattr(obj.event, 'other', xmldetail)

            return obj
        except Exception as e:
            raise e
    def _get_method_in_method_list(self, method_list: List[callable], expected_class_name: str) -> callable:
        if len(method_list) == 1:
            return method_list[0]

        elif len(method_list) > 1:
            for method in method_list:
                # required due to pythons privacy conventions
                if method.__self__.__class__.__name__.lower() == expected_class_name.lower():
                    return method
                else:
                    pass
            raise AttributeError(expected_class_name + ' does not have specified attribute')

        else:
            raise AttributeError(expected_class_name + ' does not have specified attribute')
