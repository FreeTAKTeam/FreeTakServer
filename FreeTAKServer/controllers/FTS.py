import multiprocessing
from FreeTAKServer.controllers.CreateStartupFilesController import CreateStartupFilesController
from FreeTAKServer.controllers.Orchestrator import Orchestrator
from FreeTAKServer.controllers.DataPackageServer import FlaskFunctions
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
import time
loggingConstants = LoggingConstants()
logger = CreateLoggerController("FTS").getLogger()
class FTS:

    def __init__(self):
        self.CoTService = None
        self.DataPackageService = None
        self.UserCommand = None
        self.killSwitch = False
        self.CoTPoisonPill = None

    def start_CoT_service(self):
        try:
            self.CoTPoisonPill = multiprocessing.Event()
            self.CoTPoisonPill.set()
            self.CoTIP = str(
                input('enter CoT_service IP[' + str(OrchestratorConstants().IP) + ']: ')) or OrchestratorConstants().IP
            self.CoTPort = str(input('enter CoT_service Port[' + str(
                OrchestratorConstants().COTPORT) + ']: ')) or OrchestratorConstants().COTPORT
            self.CoTService = multiprocessing.Process(target=Orchestrator().start, args=(self.CoTIP, self.CoTPort, self.CoTPoisonPill))
            return 1
        except Exception as e:
            logger.error('an exception has been thrown in CoT service startup ' + str(e))
            return -1

    def stop_CoT_service(self):
        try:
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

    def check_service_status(self):
        print('Data Package Service : ' + str(self.DataPackageService.is_alive()))
        print('CoT service is_alive : ' + str(self.CoTService.is_alive()))
        return 1
    def start_data_package_service(self):
        try:

            self.APIPort = str(input('enter DataPackage_Service Port[' + str(
                DataPackageServerConstants().APIPORT) + ']: ')) or DataPackageServerConstants().APIPORT
            self.APIIP = str(input('enter DataPackage_Service IP[' + str(
                DataPackageServerConstants().IP) + ']: ')) or DataPackageServerConstants().IP
            self.DataPackageService = multiprocessing.Process(target=FlaskFunctions().startup,
                                                              args=(self.APIIP, self.APIPort))
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
            self.start_data_package_service()
            self.start_CoT_service()
            self.DataPackageService.start()
            self.CoTService.start()
            return 1
        except Exception as e:
            logger.error('there has been an exception in FTS start_all ' + str(e))
            return -1

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
                    raise Exception('error starting DataPackage Service')
            except Exception as e:
                logger.error('error in processing your request ' + str(e))

if __name__ == "__main__":
    CreateStartupFilesController()
    FTS().receive_input()