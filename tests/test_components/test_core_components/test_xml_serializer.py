from lxml import etree
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.model.load_configuration import (
    Configuration,
    ConfigurationEntry,
    Relationship,
)
from unittest.mock import MagicMock
from FreeTAKServer.components.extended.emergency.configuration.emergency_constants import (
    TYPE_MAPPINGS,
)
from FreeTAKServer.components.extended.emergency.emergency_facade import Emergency
from FreeTAKServer.components.core.type.type_facade import Type
from FreeTAKServer.components.core.domain.domain_facade import Domain
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.services.FTS import FTS
from FreeTAKServer.model.ServiceObjects.FTS import FTS as FTSModelVariables

from FreeTAKServer.controllers.services.internal_telemetry_service import (
    InternalTelemetryService,
)
import pytest
import multiprocessing

from tests.test_components.test_utils import execute_action, execute_async_action


def setup_module(module):
    fts = FTS()
    fts.register_components(FTSServiceStartupConfigObject=FTSModelVariables())
    fts.start_routing_proxy_service(FTSServiceStartupConfigObject=FTSModelVariables())
    multiprocessing.Process(
        target=InternalTelemetryService(
            1000, "error.log", "info.log", "debug.log", 40033, "127.0.0.1"
        ).main
    ).start()
    # config = InifileConfiguration("")
    # config.add_configuration(
    #    r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\configuration\routing\action_mapping.ini"
    # )


def test_xml_to_dict():
    dict_output = execute_action("XMLToDict", {})
    assert dict_output
