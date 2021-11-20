import unittest
import json
import time
import asyncio
import socketio
import requests
import concurrent.futures

import test_data
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from stdlib_extensions import CustomAssertions
from common_testing_tools import TCPClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
pool = concurrent.futures.ThreadPoolExecutor()

def get_user_uid(username, password, token):
    fts_response = get_endpoint(auth_token=token, params={"password": password, "username": username},
                                endpoint="/AuthenticateUser")
    return json.loads(fts_response.content.decode())["uid"]

def create_socketio_client(sio: socketio.Client, url: str):
    sio.connect(url=url)
    sio.emit("authenticate", data=json.dumps({"Authenticate": MainConfig.websocketkey}))
    return sio


def get_endpoint(auth_token: str, body: dict = {}, url: str = 'http://127.0.0.1:19023', params: dict = {}, endpoint: str = "/"):
    """

    Args:
        auth_token: authentication token
        body: body of get request
        url: url base to submit request
        params: the url parameters to be submitted with request
        endpoint: the endpoint to which the request is sent

    Returns: 
        object: response object

    """
    response = requests.get(url=url + endpoint, headers={'Authorization': 'Bearer ' + auth_token}, data=body,
                            params=params)
    return response

class APIServiceTest():

    def setUp(self) -> None:
        self.ip = '192.168.2.129'
        self.port = 19023
        self.url = f'http://{self.ip}:{self.port}'
        self.headers = {
                            'Authorization': 'Bearer token',
                            'Content-Type': 'application/json'
                        }

class SystemUserTest(unittest.TestCase, APIServiceTest):
    def setUp(self) -> None:
        super().setUp()
        self.sio = socketio.Client()

    def test_generate_system_user(self):
        """ generate system user with internal API and test that the response is a 200
        """
        sio = create_socketio_client(sio=self.sio, url=self.url)
        time.sleep(5)
        sio.emit("addSystemUser", data=json.dumps({"systemUsers": [
            {"Certs": "true", "Name": "testUser", "Token": "testToken",
             "Password": "testPassword", "Group": "testGroup"}]}))  # generate system user

        sio.disconnect()

    def test_get_system_user(self):
        sio = create_socketio_client(sio=self.sio, url=self.url)
        
        system_users = {}
        
        @sio.event
        def systemUsersUpdate(data):
            nonlocal system_users
            system_users = data
        
        sio.emit("systemUsers")
        
        start = time.time()
        while system_users == {} and time.time() < start+5:
            time.sleep(0.1)
        for user in system_users["SystemUsers"]:
            if user["Name"] == "testUser":
                self.assertEqual(user["Name"], "testUser")
        
        self.assertKeyValuePairInDict(key = "Name", var = "testUser", dictionary = system_users)
        
    def test_system_user_credentials(self, password="testPassword", token="testToken", username="testUser"):
        fts_response = get_endpoint(auth_token=token, params={"password": password, "username": username},
                                    endpoint="/AuthenticateUser")

        self.assertTrue(fts_response.status_code == 200)
        self.uid = json.loads(fts_response.content.decode())["uid"]

    def test_delete_system_user(self, uid: str = None):
        time.sleep(6)
        if uid is None:
            uid = get_user_uid("testPassword", "testUser", "testToken")
        sio = create_socketio_client(sio=self.sio, url=self.url)
        time.sleep(5)
        sio.emit("removeSystemUser", data=json.dumps({"systemUsers": [
            {"uid": uid}]}))  # generate system user

        sio.disconnect()

        self.test_system_user_credentials(pasword="testPassword", token="testToken", username="testUser")

class ManageKMLTest(unittest.TestCase, APIServiceTest):
    """ this class is responsible for testing all API based functionality of the
    Manage KML endpoint
    """
    def setUp(self):
        super().setUp()
        self.url = self.url + "/ManageKML"

    def test_create_address_based_kml(self):
        """ this method tests the functionality of creating address based KML packages
        
        Returns: None

        """
        url = self.url + "/postKML"
        postData = json.dumps(test_data.TestAPIData.postKMLAddress)
        response = requests.request("POST", url, headers=self.headers, data=postData)
        self.assertTrue(response.status_code == 200)

class ManageVideoStreamTest(APIServiceTest, unittest.TestCase):
    """ this class is responsible for testing all API based functionality of the
    ManageVideoStream endpoint

    """

    def setUp(self):
        super().setUp()
        self.url = self.url + "/ManageVideoStream"

    def test_post_video_streams(self):
        """ this method tests the functionality of creating a video stream within the server

            Returns: None

        """
        url = self.url + "/postVideoStream"
        postData = json.dumps(test_data.TestAPIData.postVideo_streams)
        response = requests.request("POST", url, headers=self.headers, data=postData)
        self.assertTrue(response.status_code == 200)

    def test_get_video_streams(self):
        """ this method tests the functionality of creating video_streams

        Returns: None

        """
        url = self.url + "/getVideoStream"
        response = requests.request("GET", url, headers=self.headers)
        self.assertTrue(response.status_code == 200)

class ManageGeoObject(APIServiceTest, unittest.TestCase):
    """ this class is responsible for testing all API based functionality of the
    ManageGeoObject endpoint

    """

    def setUp(self):
        super().setUp()
        self.url = self.url + "/ManageGeoObject"

    def test_post_geoObject(self):
        """ this method tests the functionality of creating geo objects

        Returns:

        """
        url = self.url + "/postGeoObject"
        postData = json.dumps(test_data.TestAPIData().postGeoObject)
        response = requests.request("POST", url, headers=self.headers, data = postData)
        self.assertTrue(response.status_code == 200)

    def test_put_geoObject(self):
        """this method tests the functionality of updating an existing geoObject

        Returns:

        """
        # post initial geoobject
        url = self.url + "/postGeoObject"
        postData = json.dumps(test_data.TestAPIData().postGeoObject[0])
        response = requests.request("POST", url, headers=self.headers, data=postData)
        uid = response.content
        # update previously posted geoobject
        putData = test_data.TestAPIData().putGeoObject
        putData["uid"] = str(uid)
        putData = json.dumps(putData)
        result = pool.submit(asyncio.run, listen_for_cot(uid=uid))
        response = requests.request("PUT", url, headers=self.headers, data=putData)
        output = result.result()
        self.assertTrue(response.status_code == 200 and output)

class ManagePresence(APIServiceTest, unittest.TestCase):
    """ this class is responsible for testing all API based functionality of the
    ManagePresence endpoint

    """

    def setUp(self):
        super().setUp()
        self.url = self.url + "/ManagePresence"

    def test_high_volume_post_presence(self):
        """ this method tests the functionality of creating a large volume
        of geo objects with several connections in response to issue #198 on
        git.

        Returns:

        """
        url = self.url + "/postPresence"
        data = test_data.TestAPIData().postPresence
        postData = json.dumps(data)
        response = requests.request("POST", url, headers=self.headers, data=postData)
        uid = str(response.content)
        #client = TCPClient(ip=self.ip, port=15777)
        #client.connect()
        #time.sleep(0.5)
        for x in range(6000):
            data = test_data.TestAPIData().putPresence
            data["uid"] = uid
            url = self.url + "/putPresence"
            putData = json.dumps(data)
            response = requests.request("PUT", url, headers=self.headers, data=putData)
            self.assertTrue(response.status_code == 200)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ManageVideoStreamTest)
    unittest.TextTestRunner().run(suite)
