from email import header
from urllib import response
import FreeTAKServer.controllers.services.RestAPI

from unittest import TestCase, mock
import requests


class Test_getGeoObject(TestCase):
    mock_query_output = mock.MagicMock()
    mock_query_output.side_effect = []

    mock_dbController = mock.MagicMock()
    mock_dbController.queryCoT = mock_query_output

    def setUp(self) -> None:
        self.app = FreeTAKServer.controllers.services.RestAPI.app
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

    @mock.patch('FreeTAKServer.controllers.services.RestAPI.dbController', mock_dbController)
    def test_basic_request(self):
        response = self.client.get('/ManageGeoObject/getGeoObject', headers={"Authorization": "Bearer token"})
        self.mock_dbController.query_CoT.assert_called_once()
        assert response.status_code == 200

    @mock.patch('FreeTAKServer.controllers.services.RestAPI.dbController', mock_dbController)
    def test_type_filtering(self):
        response = self.client.get('/ManageGeoObject/getGeoObject', query_string={"attitude": "hostile"})
        self.mock_dbController.query_CoT.assert_called_once()
        print(response)

