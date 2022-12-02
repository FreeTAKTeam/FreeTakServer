import unittest
from defusedxml import ElementTree as etree

from FreeTAKServer.model.FTSModel.Event import Event

from FreeTAKServer.controllers.serializers.test_data import TestData
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.controllers.serializers.protobuf_serializer import ProtobufSerializer
from FreeTAKServer.controllers.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.parsers.JsonController import JsonController
from FreeTAKServer.controllers.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.controllers.RestMessageControllers.SendChatController import SendChatController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.serializers.SqlAlchemyObjectController import SqlAlchemyObjectController
#from FreeTAKServer.controllers.RestMessageControllers.SendEmergencyController import SendEmergencyController

def compare_model_objects(model_object_a, model_object_b):
    if model_object_a == model_object_b:
        return True
    else:
        return False

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

    def test_sqlalchemy_serialization(self, model_object_array = []):
        """
        this test validates the functionality of the sqlalchemy serialization, by first generating the sqlAlchemy object from
        a given model object and then regenerating the original model object
        Returns:

        """
        if not model_object_array:
           model_object_array = TestData().test_data_arr

        for model_object in model_object_array:
            # generate and add sqlalchemy object to database
            contr = DatabaseController()
            contr.create_CoT(model_object)

            # query object from db
            sqlAlchemyObject = contr.query_CoT(f'uid="{model_object.getuid()}"')[0]

            # convert sql alchemy object to model object
            modelObjectGenerated = SqlAlchemyObjectController().convert_sqlalchemy_to_modelobject(sqlAlchemyObject, model_object)

            self.assertTrue(compare_model_objects(model_object, modelObjectGenerated))

    def test_xml_serialization(self):
        """
        test new serialization in contrast with legacy serializer to ensure compatibility
        """
        # test geochats
        xmlstring = '<event version="2.0" uid="GeoChat.ANDROID-359975090666199.FEATHER.27d8ef23-8578-4cb4-8f53-02f5dc150cd2" type="b-t-f" how="h-g-i-g-o" start="2021-01-03T19:01:35.472Z" time="2021-01-03T19:01:35.472Z" stale="2021-01-04T19:01:35.472Z"><detail><__chat id="S-1-5-21-2720623347-3037847324-4167270909-1002" parent="RootContactGroup" chatroom="FEATHER" groupOwner="false"><chatgrp uid0="ANDROID-359975090666199" uid1="S-1-5-21-2720623347-3037847324-4167270909-1002" id="S-1-5-21-2720623347-3037847324-4167270909-1002"/></__chat><link uid="ANDROID-359975090666199" relation="p-p" type="a-f-G-E-V-A"/><remarks time="2021-01-03T19:01:35.472Z" source="BAO.F.ATAK.ANDROID-359975090666199" to="S-1-5-21-2720623347-3037847324-4167270909-1002">at VDO</remarks><__serverdestination destinations="192.168.2.66:4242:tcp:ANDROID-359975090666199"/><marti><dest callsign = "WOLF"/><dest callsign="GALLOP"/><dest callsign="FEATHER"/></marti></detail><point le="9999999.0" ce="3.2" hae="22.958679722315807" lon="-66.10803" lat="43.855711"/></event>'
        # xmlstring = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><event version="2.0" uid="03Z0170972" type="a-f-A-M-H-Q" time="2021-06-17T19:08:19.699Z" start="2021-06-17T19:08:19.699Z" stale="2021-06-18T19:08:23.199Z" how="m-g"><point lat="43.85566678637877" lon="-66.10800161079035" hae="0.11165844181401496" ce="0.0" le="0.0" /><detail> <contact callsign="UAS-NOVA" /><sensor elevation="0.0" vfov="66.0" north="226.70000076293945" roll="0.0" range="300" azimuth="46.0" model="Phantom 3 Advanced Camera" fov="81.0" type="r-e" version="0.6" /></detail></event>'

        fts_obj = XmlSerializer().from_format_to_fts_object(xmlstring, Event.GeoChat())
        #fts_obj = XmlSerializer().from_format_to_fts_object(xmlstring, Event.DroneSensor())
        obj = XmlSerializer().from_fts_object_to_format(fts_obj)
        print(etree.tostring(obj).decode())
        # legacyftsobj = XMLCoTController().serialize_CoT_to_model(Event.GeoChat(), etree.fromstring(xmlstring))
        legacy_string = XMLCoTController().serialize_model_to_CoT(fts_obj)
        self.assertEqual(legacy_string.decode(), etree.tostring(obj).decode())

    def test_xml_other_serialization(self):
        from FreeTAKServer.model.RawCoT import RawCoT
        from FreeTAKServer.controllers.SpecificCoTControllers.SendOtherController import SendOtherController
        rc = RawCoT()
        xmlstring = '<event version="2.0" uid="ANDROID-BC:7F:A4:0F:D2:7D" type="a-f-G-U-C-I" time="2021-12-23T16:25:08.350Z" start="2021-12-23T16:25:08.350Z" stale="2021-12-23T16:26:23.350Z" how="m-g">    <point lat="0.0" lon="0.0" hae="0.0" ce="9999999" le="9999999" />    <detail /></event>'
        # xmlstring = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><event version="2.0" uid="03Z0170972" type="a-f-A-M-H-Q" time="2021-06-17T19:08:19.699Z" start="2021-06-17T19:08:19.699Z" stale="2021-06-18T19:08:23.199Z" how="m-g"><point lat="43.85566678637877" lon="-66.10800161079035" hae="0.11165844181401496" ce="0.0" le="0.0" /><detail> <contact callsign="UAS-NOVA" /><sensor elevation="0.0" vfov="66.0" north="226.70000076293945" roll="0.0" range="300" azimuth="46.0" model="Phantom 3 Advanced Camera" fov="81.0" type="r-e" version="0.6" /></detail></event>'
        rc.xmlString = xmlstring
        sendothercontroller = SendOtherController(rc)
        fts_obj = XmlSerializer().from_format_to_fts_object(xmlstring, Event.Other())
        # fts_obj = XmlSerializer().from_format_to_fts_object(xmlstring, Event.DroneSensor())
        obj = XmlSerializer().from_fts_object_to_format(fts_obj)
        print(etree.tostring(obj).decode())
        # legacyftsobj = XMLCoTController().serialize_CoT_to_model(Event.GeoChat(), etree.fromstring(xmlstring))
        legacy_string = XMLCoTController().serialize_model_to_CoT(fts_obj)
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