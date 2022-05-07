from email import header
from urllib import response
import json

import FreeTAKServer.controllers.services.RestAPI

from unittest import TestCase, mock
import requests


class Test_postSystemUser(TestCase):
    """ this class is responsible for testing use cases related to the post
    system user endpoint
    """
    mock_query_output = mock.MagicMock()
    mock_query_output.side_effect = None

    mock_getStatus = mock.MagicMock()
    mock_getStatus.TCPDataPackageService.TCPDataPackageServiceIP = "0.0.0.0"

    FreeTAKServer.controllers.services.RestAPI.getStatus = mock.MagicMock("getStatus")
    FreeTAKServer.controllers.services.RestAPI.getStatus.return_value = mock_getStatus
    
    FreeTAKServer.controllers.services.RestAPI.APIPipe =  mock.MagicMock("APIPipe")
    FreeTAKServer.controllers.services.RestAPI.APIPipe.put =  mock.MagicMock("put")


    mock_CommandPipe = mock.MagicMock()
    mock_CommandPipe.side_effect = None

    mock_dbController = mock.MagicMock()
    FreeTAKServer.controllers.services.RestAPI.dbController.create_datapackage = mock.MagicMock("create_datapackage")
    FreeTAKServer.controllers.services.RestAPI.dbController.create_systemUser = mock.MagicMock("create_systemUser")

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
    def test_basic_request_with_cert(self):
        """ this method tests the use case of a simple request to create a user with a certificate
        """
        response = self.client.post('/ManageSystemUser/postSystemUser', headers={"Authorization": "Bearer token"}, json=json.dumps({"systemUsers":[{"Name":"dan", "Group":"Yellow", "Token":"token", "Password": "psw1", "Certs":"true", "DeviceType": "mobile" }]}), content_type='application/json')
        #self.mock_certificate_generation_controller.generate_standard_zip.assert_called_once()
        FreeTAKServer.controllers.services.RestAPI.dbController.create_systemUser.assert_called_once()
        FreeTAKServer.controllers.services.RestAPI.dbController.create_datapackage.assert_called_once()
        assert response.status_code == 200

    @mock.patch('FreeTAKServer.controllers.services.RestAPI.dbController', mock_dbController)
    def test_basic_request_without_cert(self):
        """ this method tests the use case of a simple request to create a user without a certificate
        """
        response = self.client.post('/ManageSystemUser/postSystemUser', headers={"Authorization": "Bearer token"}, json=json.dumps({"systemUsers":[{"Name":"dan", "Group":"Yellow", "Token":"token", "Password": "psw1", "Certs":"false", "DeviceType": "mobile" }]}), content_type='application/json')
        #self.mock_certificate_generation_controller.generate_standard_zip.assert_called_once()
        FreeTAKServer.controllers.services.RestAPI.dbController.create_systemUser.assert_called_once()
        assert response.status_code == 200