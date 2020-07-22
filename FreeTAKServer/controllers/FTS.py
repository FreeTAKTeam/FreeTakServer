import multiprocessing
import threading
from FreeTAKServer.controllers.CreateStartupFilesController import CreateStartupFilesController
from FreeTAKServer.controllers.Orchestrator import Orchestrator
from FreeTAKServer.controllers.DataPackageServer import FlaskFunctions
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.AsciiController import AsciiController
from FreeTAKServer.controllers.RestAPI import RestAPI
import time
loggingConstants = LoggingConstants()
logger = CreateLoggerController("FTS").getLogger()


class FTS:

    def __init__(self):
        self.CoTService = None
        self.DataPackageService = None
        self.UserCommand = None
        self.killSwitch = False
        self.ReceiveConnectionsReset = None
        self.CoTPoisonPill = None
        self.ClientDataPipe = None
        self.clientArray = []
        self.socketCount = 0
        self.clientInformationArray = []
        logger.propagate = True
        logger.info('something')

    def start_restAPI_service(self):
        try:
            self.RestAPIPipe, self.RestAPIOrchestratorPipe = multiprocessing.Pipe()
            self.RestAPIProcess = multiprocessing.Process(target=RestAPI().startup, args=(self.RestAPIPipe,))
            self.RestAPIProcess.start()
            return 1
        except Exception as e:
            logger.error('There has been an exception thrown in the startup of the restAPI service '+str(e))
            return -1

    def start_CoT_service(self):
        try:
            self.ClientDataPipe, ClientDataPipeParentChild = multiprocessing.Pipe()
            threading.Thread(target=self.receive_data_from_CoT_service_thread, daemon=True).start()
            self.CoTPoisonPill = multiprocessing.Event()
            self.CoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.CoTIP = str(
                input('enter CoT_service IP[' + str(OrchestratorConstants().IP) + ']: ')) or OrchestratorConstants().IP
            self.CoTPort = input('enter CoT_service Port[' + str(OrchestratorConstants().COTPORT) + ']: ') or int(OrchestratorConstants().COTPORT)
            self.CoTPort = int(self.CoTPort)
            self.CoTService = multiprocessing.Process(target=Orchestrator().start, args=(self.CoTIP, self.CoTPort, self.CoTPoisonPill, ClientDataPipeParentChild, self.ReceiveConnectionsReset, self.RestAPIOrchestratorPipe))
            self.CoTService.start()
            return 1
        except Exception as e:
            logger.error('an exception has been thrown in CoT service startup ' + str(e))
            return -1

    def stop_CoT_service(self):
        try:
            self.ClientDataPipe.close()
            self.CoTPoisonPill.clear()

            time.sleep(0.1)
            if self.CoTService.is_alive():
                self.CoTService.terminate()
                self.CoTService.join()
            else:
                self.CoTService.join()
        except Exception as e:
            logger.error("there's been an exception in the stopping of CoT Service " + str(e))
            return -1
        return 1

    def start_data_package_service(self):
        try:

            self.APIPort = str(input('enter DataPackage_Service Port[' + str(
                DataPackageServerConstants().APIPORT) + ']: ')) or DataPackageServerConstants().APIPORT
            self.APIPort = int(self.APIPort)
            self.APIIP = str(input('enter DataPackage_Service IP[' + str(
                DataPackageServerConstants().IP) + ']: ')) or DataPackageServerConstants().IP
            self.DataPackageService = multiprocessing.Process(target=FlaskFunctions().startup,
                                                              args=(self.APIIP, self.APIPort))
            self.DataPackageService.start()
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error('there has been an exception in the indevidual starting of the Data Packages Service')
            return -1

    def stop_data_package_service(self):
        try:
            self.DataPackageService.terminate()
        except Exception as e:
            logger.error("there's been an exception in the termination of DataPackage Service " + str(e))
            return -1
        try:
            self.DataPackageService.join()
        except Exception as e:
            logger.error("there's been an exception in the joining of DataPackage Service " + str(e))
            return -1
        return 1

    def start_all(self):
        try:
            self.start_restAPI_service()
            self.start_data_package_service()
            self.start_CoT_service()
            return 1
        except Exception as e:
            logger.error('there has been an exception in FTS start_all ' + str(e))
            return -1

    def restart_receive_connection_process(self):
        self.ReceiveConnectionsReset.set()
        return 1

    def receive_data_from_CoT_service_thread(self):
        while True:
            found = 0
            try:
                data = self.ClientDataPipe.recv()
                self.socketCount = data[2]
                self.clientInformationArray = data[3]
                if data[0] == 'add':
                    self.clientArray.append(data[1])
                else:
                    for client in self.clientArray:
                        if client.ID == data[1].ID:
                            self.clientArray.remove(client)
                            found = 1
                        else:
                            pass
                    if found == 0:
                        for client in self.clientArray:
                            if client.IP == data[1].IP and client.modelObject.m_detail.m_Contact.callsign == data[1].modelObject.m_detail.m_Contact.callsign:
                                self.clientArray.remove(client)
                                found = 1
                            else:
                                pass
                    else:
                        pass
            except Exception as e:
                pass

    def help(self):
        print('to begin all services type: start_all')
        print('to begin CoT service type: start_CoT_service')
        print('to begin data package service  type: start_data_package_service')
        print('to terminate all services type: stop_all')
        print('to terminate CoT service type: stop_CoT_service')
        print('to begin data package service type: stop_data_package_service')
        print('to check the status of the services type: check_service_status')
        print('to show connected user information type: show_users')
        print('to kill the full server type: kill')
        print('if the server has stopped accepting connections try this: restart_receive_connection_process')

    def check_service_status(self):
        print('Data Package Service : ' + str(self.DataPackageService.is_alive()))
        print('CoT service is_alive : ' + str(self.CoTService.is_alive()))
        return 1

    def show_client_array(self):
        print(self.clientInformationArray)
        print('length is ' + len(self.clientInformationArray))
        return 1

    def show_users(self):
        data = [['callsign', 'team', 'ip']]
        for client in self.clientArray:
            data.append([client.modelObject.m_detail.m_Contact.callsign, client.modelObject.m_detail.m___Group.name, client.IP[0]])
        col_width = max(len(word) for row in data for word in row) + 2  # padding
        for row in data:
            print("".join(word.ljust(col_width) for word in row))
        print('total sockets: '+str(self.socketCount))
        return 1

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
            logger.error('there has been an exception in FTS verifying output ' + str(e))
            return False

    def stop_all(self):
        try:
            DataPackageServiceOutput = self.stop_data_package_service()
            if self.verify_output(DataPackageServiceOutput):
                pass
            else:
                raise Exception('error stopping DataPackage Service')
            CoTServiceOutput = self.stop_CoT_service()
            if self.verify_output(CoTServiceOutput):
                pass
            else:
                raise Exception('error stopping CoT Service')
            return 1
        except Exception as e:
            logger.error('there has been an exception in FTS stop_all ' + str(e))
            return -1

    def kill(self):
        try:
            self.killSwitch = True
            return 1
        except Exception as e:
            logger.error('error in kill function '+str(e))

    def empty(self):
        return 1

    def receive_input(self):
        AsciiController().ascii()
        while self.killSwitch == False:
            try:
                self.UserCommand = str(input('FTS$ ')) or 'empty'
                try:
                    function = getattr(self, self.UserCommand)
                except:
                    logger.error('this is not a valid command')
                functionOutput = function()
                if self.verify_output(functionOutput):
                    pass
                else:
                    raise Exception('function returned bad data')
            except Exception as e:
                logger.error('error in processing your request ' + str(e))
        self.stop_all()


if __name__ == "__main__":
    CreateStartupFilesController()
    FTS().receive_input()
