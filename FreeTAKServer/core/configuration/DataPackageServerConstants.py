import os
import pathlib
from FreeTAKServer.core.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class DataPackageServerConstants:
    def __init__(self):
        # http server config
        self.DATABASE = 'FreeTAKServerDataPackageDataBase.db'
        self.APIPORT = '8080'
        self.DEFAULTRETURN = 'other'
        self.GET = 'GET'
        self.PUT = 'PUT'
        self.POST = 'POST'
        self.DATAPACKAGEFOLDER = 'FreeTAKServerDataPackageFolder'
        self.HTTPDEBUG = False
        self.HTTPMETHODS = ['POST', 'GET', 'PUT']
        self.IP = "0.0.0.0"
        self.versionInfo = config.version
        self.NodeID = 'FTS'
        #self.VERSIONJSON = '{"version":"3","type":"ServerConfig", "data":{"version": "%s", "api": "3","hostname":"%s"}, "nodeId":"%s"}' % (
        #    self.versionInfo, "0.0.0.0", self.NodeID)
        self.VERSIONJSON = '{"version":"3","type":"ServerConfig","data":{"version":"4.7.20-RELEASE","api":"3","hostname":"%s"},"nodeId":"%s"}' % (
            "0.0.0.0", self.NodeID)