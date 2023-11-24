from unittest.mock import patch
from FreeTAKServer.components.extended.excheck.excheck_facade import Excheck
from tests.test_components.misc import ComponentTest
from tests.test_components.test_excheck_component.test_excheck_checklist_controller_schemas import TEST_START_CHECKLIST_SCHEMA
from tests.test_components.test_excheck_component.test_excheck_template_controller_schemas import TEST_CREATE_TEMPLATE
from tests.test_components.core_mocks.enterprise_sync_mocks import create_enterprise_sync_metadata
from digitalpy.core.main.object_factory import ObjectFactory
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.configuration import MainConfig as MainConfigClass
import pathlib

config = MainConfig.instance()

@patch("FreeTAKServer.core.enterprise_sync.controllers.enterprise_sync_database_controller.EnterpriseSyncDatabaseController.create_enterprise_sync_data_object")
def test_start_checklist(create_enterprise_sync_data_object_mock):
    setup = ComponentTest(TEST_CREATE_TEMPLATE, mock_sub_actions=False, include_base_components=True, included_external_components=[pathlib.Path(MainConfigClass.MAINPATH, "component\\extended\\mission")])
    
    facade = Excheck(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    # setup mocks and data
    
    create_enterprise_sync_data_object_mock.return_value = create_enterprise_sync_metadata()

    facade.create_template(**setup.request.get_values())