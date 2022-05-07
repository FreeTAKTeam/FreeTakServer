from email import header
from urllib import response
import json

import FreeTAKServer.controllers.services.RestAPI

from unittest import TestCase, mock
import requests


class Test_putSystemUser(TestCase):
    """ this class is responsible for testing use cases related to the put
    system user endpoint
    """
    mock_query_output = mock.MagicMock()
    mock_query_output.side_effect = None

    mock_dbController = mock.MagicMock()
    FreeTAKServer.controllers.services.RestAPI.dbController.update_systemUser = mock.MagicMock("update_systemUser")

    mock_certgen_output = mock.MagicMock()
    mock_certgen_output.side_effect = None

    #mock_certificate_generation_controller = mock.MagicMock()
    #mock_certificate_generation_controller.generate_wintak_zip = mock_certgen_output

    mock_certificate_generation_controller = mock.MagicMock()
    mock_certificate_generation_controller.generate_standard_zip = mock_certgen_output

    def setUp(self) -> None:
        self.app = FreeTAKServer.controllers.services.RestAPI.app
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

    @mock.patch('FreeTAKServer.controllers.certificate_generation', mock_certificate_generation_controller)
    @mock.patch('FreeTAKServer.controllers.services.RestAPI.dbController', mock_dbController)
    def test_basic_request(self):
        """ this method tests the use case of a simple request to update a user
        """
        response = self.client.put('/ManageSystemUser/putSystemUser', headers={"Authorization": "Bearer token"}, json=json.dumps({"systemUsers":[{"uid": 1, "Name":"dan", "Group":"Yellow", "Token":"token", "Password": "psw1", "Certs":"true"}]}), content_type='application/json')
        #self.mock_certificate_generation_controller.generate_standard_zip.assert_called_once()
        assert response.status_code == 200
        FreeTAKServer.controllers.services.RestAPI.dbController.update_systemUser.assert_called_once()        

