from email import header
from urllib import response
import FreeTAKServer.controllers.services.RestAPI

import json
from unittest import TestCase, mock
import requests


class Test_deleteSystemUser(TestCase):
    """ this class is responsible for testing use cases related to the delete
    system user endpoint
    """

    mock_query_output = mock.MagicMock()
    mock_query_output.side_effect = [None]

    mock_remove_output = mock.MagicMock()
    mock_remove_output.side_effect = None

    mock_rmtree_output = mock.MagicMock()
    mock_rmtree_output.side_effect = None

    mock_no_return = mock.MagicMock()
    mock_no_return.remove = mock_remove_output
    mock_no_return.rmtree = mock_rmtree_output

    mock_dbController = mock.MagicMock()
    mock_dbController.queryCoT = mock_query_output

    mock_certgen_output = mock.MagicMock()
    mock_certgen_output.side_effect = None

    mock_certificate_generation_controller = mock.MagicMock()
    mock_certificate_generation_controller.revoke_certificate = mock_certgen_output

    FreeTAKServer.controllers.services.RestAPI.dbController.remove_datapackage = mock.MagicMock("remove_datapackage")

    def setUp(self) -> None:
        self.app = FreeTAKServer.controllers.services.RestAPI.app
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

    @mock.patch('FreeTAKServer.controllers.certificate_generation', mock_certificate_generation_controller)
    @mock.patch('FreeTAKServer.controllers.services.RestAPI.dbController', mock_dbController)
    @mock.patch('FreeTAKServer.controllers.services.RestAPI.os', mock_no_return)
    @mock.patch('FreeTAKServer.controllers.services.RestAPI.shutil', mock_no_return)
    def test_basic_request(self):
        """ this method tests the use case of a simple request to delete a user
        """
        response = self.client.delete('/ManageSystemUser/deleteSystemUser', headers={"Authorization": "Bearer token"}, json={"systemUsers":[{"uid": 1}]}, content_type='application/json')
        FreeTAKServer.controllers.services.RestAPI.dbController.remove_systemUser.assert_called_once()
        FreeTAKServer.controllers.services.RestAPI.dbController.remove_datapackage.assert_called_once()
        assert response.status_code == 200

