from digitalpy.core.object_factory import ObjectFactory
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.object_factory import ObjectFactory
from unittest.mock import MagicMock
from FreeTAKServer.components.extended.emergency.configuration.emergency_constants import (
    TYPE_MAPPINGS,
)
from FreeTAKServer.components.extended.emergency.emergency_facade import Emergency
from FreeTAKServer.components.core.type.type_facade import Type
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from lxml import etree
import pathlib
from multiprocessing import Process

from FreeTAKServer.controllers.services.Orchestrator import Orchestrator


class MockMessage:
    type = ""


def setup_module(module):
    config = InifileConfiguration("")
    config.add_configuration(
        str(pathlib.PurePath(pathlib.Path(__file__).parent.parent.parent.parent.absolute(), "FreeTAKServer/configuration/routing/action_mapping.ini"))
        # r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\configuration\routing\action_mapping.ini"
    )

    factory = DefaultFactory(config)

    ObjectFactory.configure(factory)
    ObjectFactory.register_instance("configuration", config)

    # factory instance is registered for use by the routing worker so that
    # the instances in the instance dictionary can be preserved when the
    # new object factory is instantiated in the sub-process
    ObjectFactory.register_instance("factory", factory)

    Type(None, None, None, None).register(config)

    Emergency(None, None, None, None).register(config)

    routing_proxy = ObjectFactory.get_instance("RoutingProxy")
    proc = Process(target=routing_proxy.begin_routing)
    proc.start()


def test_emergency_alert():

    test_data = '<event version="2.0" uid="S-1-5-21-2720623347-3037847324-4167270909-1002-9-1-1" type="b-a-o-tbl" time="2022-08-13T01:30:40.83Z" start="2022-08-13T01:30:40.83Z" stale="2022-08-13T01:40:40.83Z" how="h-e"><point lat="27.0196007365431" lon="-41.1839609383656" hae="9999999" ce="9999999" le="9999999" /><detail><remarks>CALL 911 NOW</remarks><link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" relation="p-p" /><contact callsign="DATA-Alert" /><emergency type="Alert">DATA</emergency></detail></event>'
    mock_message = MockMessage()
    mock_message.xmlString = test_data
    mock_message.clientInformation = "test"

    mock_client = MagicMock()

    orchestrator_instance = Orchestrator()

    orchestrator_instance.component_handler(
        mock_message,
    )

    orchestrator_instance.broadcast_component_responses()

    test_case_len = len(''.join(mock_client.send.call_args[0][0].decode().split()))
    test_data_len = len(''.join(etree.tostring(etree.fromstring(test_data)).decode().split()))

    assert test_case_len == test_data_len