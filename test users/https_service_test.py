import unittest
import requests
import socketio
import uuid
import random

def send_ssl_get_request(url: str, certs: tuple = (
        r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\certs\Client.pem",
        r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\certs\Client.key")):
    """ send an SSL encrypted request to FTS with defined body, endpoint and cert
    """
    return requests.get(url=url, cert=certs, verify=False)

def send_ssl_post_request(url: str, data=None, headers=None, params=None, files = None, certs: tuple = (r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\certs\Client.pem",
                                                          r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\certs\Client.key")):
    if params is None:
        params = {}
    requests.post(url= url, data= data, verify= False, params=params, files=files, headers = headers, certs = certs)

def upload_dp(address, uid = str(uuid.uuid4()), data_file = r"C:\Users\natha\PycharmProjects\FreeTakServer\test users\test_data\example.txt"):
    send_ssl_post_request(url = address+"Marti/sync/missionupload", params={"filename": str(random.randint(1, 10000)), "creatorUid": "testing", "hash": uid}, files=[('assetfile', ("example.txt", open(data_file, 'r')))])

class HTTPSServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        """
        self.url = "https://204.48.30.216:8443/"

    def test_is_alive(self):
        response = send_ssl_get_request(url=self.url)
        self.assertTrue(response.status_code == 200)

    def test_download_dp(self):
        """ test that downloading datapackages is functional

        generate a dp on the FTS machine and then attempt to download this file finally validate
        the downloaded file with the sent file

        """
        data_file = r"C:\Users\natha\PycharmProjects\FreeTakServer\test users\test_data\example.txt"
        dp_uid = str(uuid.uuid4())
        upload_dp(address=self.url, uid=dp_uid, data_file = data_file)
        response = send_ssl_get_request(url= self.url+f"Marti/api/sync/metadata/{dp_uid}/tool")
        self.assertEqual(response.text, open(data_file, "r").read())

    def send_help_request(self):
        """ connect to FTS instance and attempt to send a request to the help endpoint
        """



if __name__ == '__main__':
    unittest.main()
