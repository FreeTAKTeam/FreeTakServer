import http.client
import json
import tabulate
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables as vars
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.ServiceObjects.FTS import FTS
from FreeTAKServer.model.ServiceObjects.RestAPIService import RestAPIService

loggingConstants = LoggingConstants()
logger = CreateLoggerController("CLI").getLogger()

json_content = vars()
json_content.default_values()
json_content.json_content()
connectionIP = str(RestAPIService().RestAPIServiceIP)
connectionPort = int(RestAPIService().RestAPIServicePort)

#TODO: standardize and abstract this
class RestCLIClient:

    def __init__(self):
        self.killSwitch = False
        self.conn = http.client.HTTPConnection(connectionIP, connectionPort)

    def check_response(self, response):
        if response.code == 200:
            return True
        else:
            return False
    def change_connection_info(self):
        global connectionIP, connectionPort
        ip = str(input('please enter desired IP for connection[' + str(connectionIP) + ']') or connectionIP)
        port = int(input('please enter desired Port for connection[' + str(connectionPort) + ']') or connectionPort)
        connectionIP = ip
        connectionPort = port
        print('connection information changed')
        return 1
    def start_CoT_service(self):
        try:
            self.CoTIP = str(
                input('enter CoT_service IP[' + str(FTS().CoTService.CoTServiceIP) + ']: ')) or FTS().CoTService.CoTServiceIP
            self.CoTPort = input('enter CoT_service Port[' + str(FTS().CoTService.CoTServicePort) + ']: ') or int(
                FTS().CoTService.CoTServicePort)
            self.CoTPort = int(self.CoTPort)
            #send start COT
            json_content.setdefaultCoTPort(self.CoTPort)
            json_content.setdefaultCoTIP(self.CoTIP)
            json_content.setdefaultCoTStatus('start')
            body = json.dumps(json_content.getJsonStatusStartAll())
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("POST", "/changeStatus",  body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            if self.check_response(response):
                print('CoT service started')
            else:
                print('CoT service startup failed')
            return 1
        except Exception as e:
            logger.error('an exception has been thrown in CoT service startup ' + str(e))
            return -1

    def stop_CoT_service(self):
        try:
            json_content.setdefaultCoTStatus('stop')
            body = json.dumps(json_content.getJsonStatusStartAll())
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("POST", "/changeStatus", body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            if self.check_response(response):
                print('CoT service stopped')
            else:
                print('CoT service stopping failed')
            return 1
        except Exception as e:
            logger.error("there's been an exception in the stopping of CoT Service " + str(e))
            return -1

    def start_data_package_service(self):
        try:

            self.APIPort = str(input('enter DataPackage_Service Port[' + str(
                DataPackageServerConstants().APIPORT) + ']: ')) or DataPackageServerConstants().APIPORT
            self.APIPort = int(self.APIPort)
            self.APIIP = str(input('enter DataPackage_Service IP[' + str(
                DataPackageServerConstants().IP) + ']: ')) or DataPackageServerConstants().IP
            #send start request
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            body = json.dumps({"TCPDataPackageService":{"IP": str(self.APIIP), "PORT": int(self.APIPort)}})
            conn.request("POST", "/TCPDataPackageService", body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            if self.check_response(response):
                print('data package service started')
            else:
                print('data package service startup failed')
            return 1
        except Exception as e:
            logger.error('there has been an exception in the indevidual starting of the Dwata Packages Service')
            return -1

    def stop_data_package_service(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("DELETE", "/TCPDataPackageService")
            response = conn.getresponse()
            if self.check_response(response):
                print('data package service stoped')
            else:
                print('data package service stop failed')
            return 1
        except Exception as e:
            logger.error("there's been an exception in the termination of DataPackage Service " + str(e))
            return -1

    def start_all(self):
        try:
            json_content.setdefaultCoTIP(input('Please enter the CoT service IP [' + str(FTS().CoTService.CoTServiceIP) + ']: ') or FTS().CoTService.CoTServiceIP)
            json_content.setdefaultCoTPort(input('Please enter the CoT service Port [' + str(FTS().CoTService.CoTServicePort) + ']: ') or FTS().CoTService.CoTServicePort)
            json_content.setdefaultDataPackagePort(input('Please enter the Data Package service Port [' + str(FTS().DataPackageService.DataPackageServicePort) + ']: ') or FTS().DataPackageService.DataPackageServicePort)
            json_content.setdefaultDataPackageIP(input('Please enter the Data Package service IP [' + str(FTS().DataPackageService.DataPackageServiceIP) + ']: ') or FTS().DataPackageService.DataPackageServiceIP)
            body = json.dumps(json_content.getJsonStatusStartAll())
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("POST", "/changeStatus", body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            conn.close()
            if self.check_response(response):
                print('server started')
            else:
                print('server startup failed')
            return 1
        except Exception as e:
            logger.error('there has been an exception in RestCLIClient start_all ' + str(e))
            return -1
    
    def stop_all(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            body = json.dumps({"CoTService": {"STATUS": "stop"},
                               "TCPDataPackageService": {"STATUS": "stop"}})
            conn.request("POST", "/changeStatus", body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            if self.check_response(response):
                print('server stopped')
            else:
                print('server stopping failed')
            return 1
        except Exception as e:
            logger.error('there has been an exception in RestCLIClient stop_all ' + str(e))
            return -1

    def add_api_user(self):
        import uuid
        conn = http.client.HTTPConnection(connectionIP, connectionPort)
        username = input('please enter the username for the new user: ')
        token = input('please enter the token for the new user: ')
        if token is None:
            token = uuid.uuid4()
        else:
            pass
        conn.request("POST", "/APIUser", body = json.dumps({'username': username, "token": token}), headers={"Content-type": "application/json", "Accept": "text/plain"})
        response = conn.getresponse()
        print('user created\n'
              'username: ' + username + '\n'
              'token: ' + token)
        return response

    def remove_api_user(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            username = input('please enter username of user to be deleted: ')
            conn.request("DELETE", "/APIUser", body = json.dumps({'username': username}), headers={"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            print('user ' + username + ' has been deleted')
            return response
        except Exception as e:
            logger.error('there has been an exception in RestCLI Client remove_api_user ' + str(e))
            return -1

    def show_api_users(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("GET", "/APIUser")
            response = conn.getresponse()
            api_users = json.loads(response.read().decode("utf-8"))
            DPArray = []
            for dict in api_users['json_list']:
                values = list(dict.values())
                DPArray.append(values)
            table = tabulate.tabulate(DPArray, headers = ["Token", "Username"], tablefmt='psql')
            print(table)
            return 1

        except Exception as e:
            logger.error('there has been an exception in RestCLI Client show_api_users ' + str(e))
            return -1

    def show_DP(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("GET", "/DataPackageTable")
            response = conn.getresponse()
            DataPackages = json.loads(response.read().decode("utf-8"))
            DPArray = []
            for dict in DataPackages['json_list']:
                values = list(dict.values())
                DPArray.append(values)
            table = tabulate.tabulate(DPArray, headers = ["Keywords", "Name", "Index", "Privacy", "Size", "SubmissionDataTime", "SubmissionUser"], tablefmt='psql')
            print(table)
            return 1

        except Exception as e:
            logger.error("there has been an exception thrown in show DP function")
            return -1

    def remove_DP(self):
        hash = input('Index of DataPackage to delete: ')
        conn = http.client.HTTPConnection(connectionIP, connectionPort)
        conn.request("DELETE", f"/DataPackageTable?Hash={hash}")
        response = conn.getresponse()
        DataPackages = json.loads(response.read().decode("utf-8"))
        if self.check_response(response):
            print('DP removed succesfully')
        else:
            print('DP removed failed')
        return 1

    def help(self):
        print('start_all: to begin all services type')
        print('start_CoT_service: to begin CoT service type')
        print('start_data_package_service: to begin data package service  type')
        print('stop_all: to terminate all services type')
        print('stop_CoT_service: to terminate CoT service type')
        print('stop_data_package_service: to begin data package service type')
        print("change_connection_info: change the address and port of the server you're connecting to")
        print('show_users: to show connected user information type')
        print('kill: terminate all the services')
        print('show_DP: to show all DataPackages on the server')
        print('remove_DP: to remove a DataPackages on the server')
        print('add_api_user: create a user for the api')
        print('remove_api_user: delete an api user')
        print('show_api_users: show a table of all api users and their associated tokens')
        return 1

    def check_service_status(self):
        pass
        return 1

    def show_client_array(self):
        print(self.clientInformationArray)
        print('length is ' + len(self.clientInformationArray))
        return 1

    def show_users(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("GET", "/Clients")
            data = conn.getresponse()
            data = data.read()
            conn.close()
            data = json.loads(data)
            data.insert(0, {'ip': 'IP', 'callsign': 'CALLSIGN', 'team': 'TEAM'})
            col_width = max(len(word) for row in data for word in row.values()) + 2  # padding
            for row in data:
                print("".join(word.ljust(col_width) for word in row.values()))
            return 1

        except Exception as e:
            print(e)

    def server_geochat(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            text = input('enter message: ')
            body = json.dumps({"detail": {'remarks': {"INTAG": text}}})
            conn.request("POST", "/SendGeoChat", body, {"Content-type": "application/json", "Accept": "application/json"})
            data = conn.getresponse()
            conn.close()
            if self.check_response(data):
                print('geochat sent')
                return 1
            else:
                return 1
                print('geochat failed to send')
        except Exception as e:
            pass

    def connection_message(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            text = input('enter message: ')
            body = json.dumps({"detail": {'remarks': {"INTAG": text}}})
            conn.request("POST", "/ConnectionMessage", body, {"Content-type": "application/json", "Accept": "application/json"})
            data = conn.getresponse()
            conn.close()
            if self.check_response(data):
                print('geochat sent')
                return 1
            else:
                print('geochat failed to send')
                return 1
        except Exception as e:
            pass

    def verify_output(self, input, example=None):
        try:
            if example == None:
                if input == None or input == -1:
                    return False
                else:
                    return True

            else:
                if isinstance(input, example):
                    return True
                else:
                    return False
        except Exception as e:
            logger.error('there has been an exception in RestCLIClient verifying output ' + str(e))
            return False

    def kill(self):
        try:
            self.killSwitch = True
            return 1
        except Exception as e:
            logger.error('error in kill function '+str(e))

    def empty(self):
        return 1

    def receive_input(self):
        conn = http.client.HTTPConnection(connectionIP, connectionPort)
        while self.killSwitch == False:
            try:
                self.UserCommand = str(input('FTS$ ')) or 'empty'
                try:
                    function = getattr(self, self.UserCommand)
                    functionOutput = function()
                    self.UserCommand = None
                    if self.verify_output(functionOutput):
                        pass
                    else:
                        raise Exception('function returned bad data')
                except Exception as e:
                    print('error in processing your request ' + str(e))
            except:
                logger.error('this is not a valid command')
        self.stop_all()


if __name__ == "__main__":
    from FreeTAKServer.controllers.AsciiController import AsciiController
    AsciiController().ascii()
    RestCLIClient().receive_input()
