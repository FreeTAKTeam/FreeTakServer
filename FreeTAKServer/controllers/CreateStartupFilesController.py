import os
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from pathlib import PurePath, Path
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
class CreateStartupFilesController:
    def __init__(self):
        self.dp_directory = PurePath(MainConfig.DataPackageFilePath)
        self.logs_directory = PurePath(MainConfig.MainPath, LoggingConstants.LOGDIRECTORY)
        self.createFolder()

    def createFolder(self):
        try:
            os.mkdir(MainConfig.MainPath)
        except:
            pass
        try:
            os.mkdir(str(MainConfig.MainPath)+"/controllers")
        except Exception as e:
            print(e)
        try:
            os.mkdir(str(self.dp_directory))
        except:
            pass
        try:
            os.mkdir(str(self.logs_directory))
        except Exception as e:
            print(e)
        try:
            os.mkdir(str(MainConfig.MainPath)+'/certs')
        except:
            pass
        try:
            os.mkdir(str(MainConfig.MainPath)+'/certs/ClientPackages')
        except:
            pass
        ERRORLOG = open(LoggingConstants().ERRORLOG, mode="w")
        ERRORLOG.close()
        HTTPLOG = open(LoggingConstants().HTTPLOG, mode="w")
        HTTPLOG.close()
        DEBUGLOG = open(LoggingConstants().DEBUGLOG, mode="w")
        DEBUGLOG.close()
        INFOLOG = open(LoggingConstants().INFOLOG, mode="w")
        INFOLOG.close()
