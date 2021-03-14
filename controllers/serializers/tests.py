import unittest

from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.controllers.serializers.protobuf_serializer import ProtobufSerializer
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.JsonController import JsonController
from FreeTAKServer.controllers.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.controllers.RestMessageControllers.SendChatController import SendChatController
#from FreeTAKServer.controllers.RestMessageControllers.SendEmergencyController import SendEmergencyController
from lxml import etree

class TestSerializers(unittest.TestCase):

    def test_json_serializer_with_geoobject_adapter(self):
        """
        test new serialization in contrast with legacy serializer to ensure compatibility
        """
        from FreeTAKServer.controllers.serializers.api_adapters.api_adapters import GeoObjectAdapter
        basejson = {
                        "attitude": "friendly",
                        "how": "nonCoT",
                        "name": "testing",
                        "latitude": "37.5677889",
                        "longitude": "12.345678",
                        "geoObject": "Ground",
                        "timeout": "120"
                    }
        jsonobj = JsonController().serialize_geoobject_post(basejson)
        simpleCoTObject = SendSimpleCoTController(jsonobj).getCoTObject()
        xml_legacy = etree.fromstring(simpleCoTObject.xmlString)
        xml_legacy.attrib['uid'] = '123'
        xml_legacy.attrib['time'] = '24'
        xml_legacy.attrib['start'] = '849'
        xml_legacy.attrib['stale'] = '3333'
        newObject = GeoObjectAdapter().from_api_to_fts_object(basejson)
        xml_updated = etree.fromstring(newObject.xmlString)
        xml_updated.attrib['uid'] = '123'
        xml_updated.attrib['time'] = '24'
        xml_updated.attrib['start'] = '849'
        xml_updated.attrib['stale'] = '3333'
        xml_legacy = etree.tostring(xml_legacy).decode()
        xml_updated = etree.tostring(xml_updated).decode()
        self.assertEqual(xml_legacy, xml_updated)

    def test_json_serializer_with_chat_adapter(self):
        from FreeTAKServer.controllers.serializers.api_adapters.api_adapters import ChatAdapter
        basejson = {
                        "message": "testing",
                        "sender": "apiuser"
                    }
        jsonobj = JsonController().serialize_chat_post(basejson)
        simpleCoTObject = SendChatController(jsonobj).getCoTObject()
        xml_legacy = etree.fromstring(simpleCoTObject.xmlString)
        xml_legacy.attrib['uid'] = '123'
        xml_legacy.attrib['time'] = '24'
        xml_legacy.attrib['start'] = '849'
        xml_legacy.attrib['stale'] = '3333'
        newObject = ChatAdapter().from_api_to_fts_object(basejson)
        xml_updated = etree.fromstring(newObject.xmlString)
        xml_updated.attrib['uid'] = '123'
        xml_updated.attrib['time'] = '24'
        xml_updated.attrib['start'] = '849'
        xml_updated.attrib['stale'] = '3333'
        xml_legacy = etree.tostring(xml_legacy).decode()
        xml_updated = etree.tostring(xml_updated).decode()
        self.assertEqual(xml_legacy, xml_updated)

    def test_json_serializer_with_presence_adapter(self):
        from FreeTAKServer.controllers.RestMessageControllers.SendPresenceController import SendPresenceController
        from FreeTAKServer.controllers.serializers.api_adapters.api_adapters import PresenceAdapter
        basejson = {
                        "how": "nonCoT",
                        "name": "testing",
                        "latitude": "34.5677889",
                        "longitude": "12.345678",
                        "role": "Team Member",
                        "team": "Cyan"
                    }
        jsonobj = JsonController().serialize_presence_post(basejson)
        simpleCoTObject = SendPresenceController(jsonobj).getCoTObject()
        xml_legacy = etree.fromstring(simpleCoTObject.xmlString)
        xml_legacy.attrib['uid'] = '123'
        xml_legacy.attrib['time'] = '24'
        xml_legacy.attrib['start'] = '849'
        xml_legacy.attrib['stale'] = '3333'
        newObject = PresenceAdapter().from_api_to_fts_object(basejson)
        xml_updated = etree.fromstring(newObject.xmlString)
        xml_updated.attrib['uid'] = '123'
        xml_updated.attrib['time'] = '24'
        xml_updated.attrib['start'] = '849'
        xml_updated.attrib['stale'] = '3333'
        xml_legacy = etree.tostring(xml_legacy).decode()
        xml_updated = etree.tostring(xml_updated).decode()
        self.assertEqual(xml_legacy, xml_updated)

    def test_json_serializer_with_emergency_adapter(self):
        from FreeTAKServer.controllers.RestMessageControllers.SendEmergencyController import SendEmergencyController
        from FreeTAKServer.controllers.serializers.api_adapters.api_adapters import EmergencyOnAdapter
        basejson = {
                        "emergencyType": "911 Alert",
                        "name": "test"
                    }
        jsonobj = JsonController().serialize_emergency_post(basejson)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        xml_legacy = etree.fromstring(EmergencyObject.xmlString)
        xml_legacy.attrib['uid'] = '123'
        xml_legacy.attrib['time'] = '24'
        xml_legacy.attrib['start'] = '849'
        xml_legacy.attrib['stale'] = '3333'
        newObject = EmergencyOnAdapter().from_api_to_fts_object(basejson)
        xml_updated = etree.fromstring(newObject.xmlString)
        xml_updated.attrib['uid'] = '123'
        xml_updated.attrib['time'] = '24'
        xml_updated.attrib['start'] = '849'
        xml_updated.attrib['stale'] = '3333'
        xml_legacy = etree.tostring(xml_legacy).decode()
        xml_updated = etree.tostring(xml_updated).decode()
        self.assertEqual(xml_legacy, xml_updated)

    def test_xml_serialization(self):
        """
        test new serialization in contrast with legacy serializer to ensure compatibility
        """
        from FreeTAKServer.model.FTSModel.Event import Event
        xmlstring = '<event version="2.0" uid="GeoChat.ANDROID-359975090666199.FEATHER.27d8ef23-8578-4cb4-8f53-02f5dc150cd2" type="b-t-f" how="h-g-i-g-o" start="2021-01-03T19:01:35.472Z" time="2021-01-03T19:01:35.472Z" stale="2021-01-04T19:01:35.472Z"><detail><__chat id="S-1-5-21-2720623347-3037847324-4167270909-1002" parent="RootContactGroup" chatroom="FEATHER" groupOwner="false"><chatgrp uid0="ANDROID-359975090666199" uid1="S-1-5-21-2720623347-3037847324-4167270909-1002" id="S-1-5-21-2720623347-3037847324-4167270909-1002"/></__chat><link uid="ANDROID-359975090666199" relation="p-p" type="a-f-G-E-V-A"/><remarks time="2021-01-03T19:01:35.472Z" source="BAO.F.ATAK.ANDROID-359975090666199" to="S-1-5-21-2720623347-3037847324-4167270909-1002">at VDO</remarks><__serverdestination destinations="192.168.2.66:4242:tcp:ANDROID-359975090666199"/><marti><dest callsign = "WOLF"/><dest callsign="GALLOP"/><dest callsign="FEATHER"/></marti></detail><point le="9999999.0" ce="3.2" hae="22.958679722315807" lon="-66.10803" lat="43.855711"/></event>'
        fts_obj = XmlSerializer().from_format_to_fts_object(xmlstring, Event.GeoChat())
        obj = XmlSerializer().from_fts_object_to_format(fts_obj)
        print(etree.tostring(obj).decode())
        legacyftsobj = XMLCoTController().serialize_CoT_to_model(Event.GeoChat(), etree.fromstring(xmlstring))
        legacy_string = XMLCoTController().serialize_model_to_CoT(legacyftsobj)
        self.assertEqual(legacy_string.decode(), etree.tostring(obj).decode())

    def test_from_protobuf_serialization(self):
        from FreeTAKServer.model.FTSModel.Event import Event
        from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent
        import lxml
        protobufString = b'\n\x83\x04\x08\xbe\xb9\xfb\x85\xeb.\x10\xbe\xb9\xfb\x85\xeb.\x18\x96\xab\x92\x86\xeb.!\xaf\xf6b\x88\\d<@) {Mcr\x1aG\xc01\x00\x00\x00\xe0\xcf\x12cA9\x00\x00\x00\xe0\xcf\x12cAA\x00\x00\x00\xe0\xcf\x12cAJ.S-1-5-21-2720623347-3037847324-4167270909-1002R\x0ba-f-G-U-C-IZ\x03h-eb\xfa\x02<detail><takv version="4.0.0.117" platform="WinTAK-CIV" os="Microsoft Windows 10 Home" device="Micro-Star International Co., Ltd MS-7C02"/><contact callsign="FEATHER" endpoint="*:-1:stcp"/><uid Droid="FEATHER"/><__group name="Cyan" role="Team Member"/><_flow-tags_ TAK-Server-c0581fed97ff4cb89eb8666a8794670cc9f77ddb-badf-48da-abe7-84545ecda69d="2020-12-29T23:04:27Z"/></detail>hd'
        # protobufString2 = b'"\x00\x00\x00="\x12;\x08\x01\x12.S-1-5-21-2720623347-3037847324-4167270909-1002\x1a\x07FEATHER'
        protobufObj = FederatedEvent()
        protobufObj.ParseFromString(protobufString)
        # protobufObj.ParseFromString(protobufString2)
        #y = [name.name for name in protobufObj.event.DESCRIPTOR.fields]
        fts_obj = ProtobufSerializer().from_format_to_fts_object(protobufObj, Event.Connection())
        z = lxml.etree.tostring(XmlSerializer().from_fts_object_to_format(fts_obj))
        1 == 1

    def test_to_protobuf_serialization(self):
        from FreeTAKServer.model.FTSModel.Event import Event
        xmlstring = '<event version="2.0" uid="ANDROID-R5CN70EYKQH" type="a-f-G-U-C" how="h-e" start="2020-12-24T18:16:22.325Z" time="2020-12-24T18:16:22.325Z" stale="2020-12-24T18:22:37.325Z"><detail><__group name="Teal" role="Team Member"/><status battery="76"/><takv version="4.2.0.4 (47e136dd).1607456856-CIV" platform="ATAK-CIV" device="SAMSUNG SM-N986U" os="29"/><track course="159.1462509079387" speed="0.0"/><contact callsign="SPAC3SLOTH" endpoint="*:-1:stcp" /><uid Droid="SPAC3SLOTH"/><precisionlocation altsrc="GPS" geopointsrc="GPS"/></detail><point le="9999999.0" ce="11.0" hae="178.84407323983876" lon="-76.675505" lat="39.664392"/></event>'
        fts_obj = XmlSerializer().from_format_to_fts_object(xmlstring, Event.Connection())
        y = ProtobufSerializer().from_fts_object_to_format(fts_obj)
        1 == 1