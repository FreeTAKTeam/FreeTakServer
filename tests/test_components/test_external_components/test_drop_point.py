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
        str(pathlib.PurePath(pathlib.Path(__file__).parent.parent.parent.parent.absolute(), "FreeTAKServer/configuration/routing/action_mapping.ini"))
    )

    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance("configuration", config)

    Type(None, None, None, None).register(config)

    DropPoint(None, None, None, None).register(config)

def test_drop_point():
    test_data = """
        <event version="2.0" uid="312609c4-a131-4bff-93d8-41cd3d7cd7f2" type="a-f-G" how="h-g-i-g-o" time="2021-12-22T13:04:59Z" start="2021-12-22T13:04:59Z" stale="2022-12-22T13:04:59Z">
            <point lat="43.8422211" lon="-65.9108380" hae="-22.48" le="9999999" ce="9999999" />
            <detail>
                <contact callsign="F.22.130459" />
                <link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" parent_callsign="DATA" relation="p-p" production_time="2021-12-22T13:04:59Z" />
                <usericon iconsetpath="COT_MAPPING_2525B/a-f/a-f-G" />
                <precisionlocation altsrc="DTED0" />
            </detail>
        </event>
    """
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
