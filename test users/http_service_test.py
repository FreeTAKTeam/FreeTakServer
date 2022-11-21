import unittest
import uuid
import random

import requests

TEST_DATA_PATH = "example.txt"

def send_get_request(url: str):
    """ send an SSL encrypted request to FTS with defined body, endpoint and cert
    """
    return requests.get(url=url, verify=False)

def send_post_request(url: str, data=None, headers=None, params=None, files = None):
    if params is None:
        params = {}
    requests.post(url= url, data= data, verify= False, params=params, files=files, headers = headers)

def upload_dp(address, uid = str(uuid.uuid4()), data_file = TEST_DATA_PATH):
    send_post_request(url = address+"Marti/sync/missionupload", params={"filename": str(random.randint(1, 10000)), "creatorUid": "testing", "hash": uid}, files=[('assetfile', ("example.txt", open(data_file, 'r')))])


class HTTPServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        """
        self.url = "http://127.0.0.1:8080/"

    def test_is_alive(self):
        response = send_get_request(url=self.url)
        self.assertTrue(response.status_code == 200)

    def test_download_dp(self):
        """ test that downloading datapackages is functional

        generate a dp on the FTS machine and then attempt to download this file finally validate
        the downloaded file with the sent file

        """
        data_file = TEST_DATA_PATH
        dp_uid = str(uuid.uuid4())
        upload_dp(address=self.url, uid=dp_uid, data_file = data_file)
        response = send_get_request(url= self.url+f"Marti/api/sync/metadata/{dp_uid}/tool")
        self.assertEqual(response.text, open(data_file, "r").read())

    def send_help_request(self):
        """ connect to FTS instance and attempt to send a request to the help endpoint
        """

if __name__ == '__main__':
    unittest.main()
