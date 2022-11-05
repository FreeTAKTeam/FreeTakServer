from lxml import etree
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.object_factory import ObjectFactory
from unittest.mock import MagicMock
from FreeTAKServer.components.extended.emergency.configuration.emergency_constants import (
    TYPE_MAPPINGS,
)
from FreeTAKServer.components.extended.emergency.emergency_facade import Emergency
from FreeTAKServer.components.core.type.type_facade import Type
from FreeTAKServer.components.core.domain.domain_facade import Domain
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.components.core.xml_serializer.xml_serializer_facade import (
    XMLSerializer,
)

from ..test_utils import execute_action


def setup_module(module):
    config = InifileConfiguration("")
    config.add_configuration(
        r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\configuration\routing\action_mapping.ini"
    )

    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance("configuration", config)

    Type(None, None, None, None).register(config)

    Domain(None, None, None, None).register(config)

    XMLSerializer(None, None, None, None).register(config)


def test_domain_health():
    test_data = '<event version="2.0" uid="S-1-5-21-2720623347-3037847324-4167270909-1002-9-1-1" type="b-a-o-tbl" time="2022-08-13T01:30:40.83Z" start="2022-08-13T01:30:40.83Z" stale="2022-08-13T01:40:40.83Z" how="h-e"><point lat="27.0196007365431" lon="-41.1839609383656" hae="9999999" ce="9999999" le="9999999" /><detail><link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" relation="p-p" /><contact callsign="DATA-Alert" /><emergency type="Alert">DATA</emergency></detail></event>'
    mock_message = MagicMock()
    mock_message.xmlString = test_data
    mock_message.clientInformation = "test"

    health_check_output = execute_action("HealthCheck", {})

    assert health_check_output["health"] == True


def test_domain_metrics():
    execute_action("TestMetrics", {})
    get_metrics_output = execute_action("GetMetrics", {})
    assert False
