from unittest.mock import patch
from FreeTAKServer.components.extended.excheck.excheck_facade import Excheck
from tests.test_components.misc import ComponentTest
from tests.test_components.test_excheck_component.test_excheck_checklist_controller_schemas import TEST_START_CHECKLIST_SCHEMA
from tests.test_components.test_mission_component.mission_model_test_utils import create_mission_cot
from digitalpy.core.main.object_factory import ObjectFactory
from FreeTAKServer.core.configuration.MainConfig import MainConfig
import pathlib

config = MainConfig.instance()

def test_start_checklist():
    setup = ComponentTest(TEST_START_CHECKLIST_SCHEMA, mock_sub_actions=False, include_base_components=True, included_external_components=[pathlib.Path(MainConfig.MAINPATH, "component\\extended\\mission")])
    
    facade = Excheck(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    # setup mission data

    facade.start_checklist(**setup.request.get_values())

    