from FreeTAKServer.components.core.COT_router.COT_router_facade import COTRouter
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.object_factory import ObjectFactory
from unittest.mock import MagicMock
from lxml import etree
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.components.core.type.type_facade import Type
from FreeTAKServer.components.core.COT_router.COT_router_facade import COTRouter


def setup_module(module):
    config = InifileConfiguration("")
    config.add_configuration(
        r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\configuration\routing\action_mapping.ini"
    )

    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance("configuration", config)

    Type(None, None, None, None).register(config)
    COTRouter(None, None, None, None).register(config)


def test_cot_received():
    test_data = '<event version="2.0" uid="3d331e11-7611-49a2-ba18-655995005627" type="a-f-G" how="h-g-i-g-o" time="2021-01-21T02:03:25Z" start="2021-01-21T02:03:25Z" stale="2022-01-21T02:03:25Z"> iieoidaoidwowa <point lat="39.3091185" lon="-29.1611324" hae="9999999" le="9999999" ce="9999999" /><detail><contact callsign="F.21.020325" /> <link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" parent_callsign="FAST" relation="p-p" production_time="2021-01-21T02:03:25Z" /><archive /><usericon iconsetpath="COT_MAPPING_2525B/a-f/a-f-G" /></detail></event>'
    mock_message = MagicMock()
    mock_message.xmlString = test_data
    mock_message.clientInformation = "test"

    mock_client = MagicMock()

    XMLCoTController(MagicMock()).determineCoTGeneral(
        mock_message, {"test": [mock_client, MagicMock()]}
    )

    assert len(mock_client.send.call_args[0][0].decode()) == len(
        etree.tostring(etree.fromstring(test_data))
    )


def test_cot_broadcast():
    pass
