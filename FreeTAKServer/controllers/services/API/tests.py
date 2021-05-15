import unittest
import threading

class Tests(unittest.TestCase):
    def test_service_info(self):
        from multiprocessing import Pipe
        from FreeTAKServer.model.ServiceObjects.FTS import FTS
        pipe1, pipe2 = Pipe(True)
        from FreeTAKServer.controllers.services.API import RestAPI
        RestAPI.CommandPipe = pipe1
        pipe2.put(FTS())
        RestAPI.show_service_info()

    def test_change_status(self):
        from FreeTAKServer.controllers.services import RestAPI
        RestAPI.changeStatus({"services": {"TCPDataPackageService":{"status":"off"}}, "ip": ""})
        
    def test_add_system_user(self):
        import json
        from FreeTAKServer.controllers.services import RestAPI
        RestAPI.addSystemUser(json.dumps({
                                "systemUsers":
                                        [
                                            {"Name": "bbrdk", "Group": "Yellow", "Token": "token", "Password": "psw1", "Certs": "true"}
                                        ]
                                }))
        
    def test_get_system_user(self):
        from FreeTAKServer.controllers.services import RestAPI
        RestAPI.systemUsers()