import pathlib
from unittest.mock import MagicMock

from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.core.object_factory import ObjectFactory
from FreeTAKServer.components.core.type.type_facade import Type
from FreeTAKServer.components.extended.drop_point.drop_point_facade import DropPoint
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from lxml import etree


def setup_module():
    config = InifileConfiguration("")
    config.add_configuration(
        str(pathlib.PurePath(pathlib.Path(__file__).parent.parent.parent.parent.absolute(), "FreeTAKServer/configuration/external_action_mapping.ini"))
    )

    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance("configuration", config)

    Type(None, None, None, None).register(config)

    DropPoint(None, None, None, None).register(config)

def test_drop_point():
    test_data = '<event version="2.0" uid="S-1-5-21-2720623347-3037847324-4167270909-1002-9-1-1" type="b-a-o-tbl" time="2022-08-13T01:30:40.83Z" start="2022-08-13T01:30:40.83Z" stale="2022-08-13T01:40:40.83Z" how="h-e"><point lat="27.0196007365431" lon="-41.1839609383656" hae="9999999" ce="9999999" le="9999999" /><detail><link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" relation="p-p" /><contact callsign="DATA-Alert" /><emergency type="Alert">DATA</emergency></detail></event>'
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
