import os
import pathlib
class vars():
   def __init__(self):
       #tcp server config
       self.dir = dir_path = os.path.dirname(os.path.realpath(__file__))
       self.PING = 'ping'
       self.GEOCHAT = 'GeoChat'
       self.FAIL = 'fail'
       self.EMPTY_BYTE = b''
       self.PORT = 8087
       self.STARTBUFFER = 32784
       self.BUFFER =513
       self.DELAY = 5
       self.IP = 'Your IP'
       self.RENEWTIME = 1
       #logging config
       self.LOGFORMAT = '%(levelname)s : %(asctime)s : %(filename)s:%(lineno)d : %(message)s'
       self.LOGNAME = 'FTS'
       self.LOGDIRECTORY = 'logs'
       self.WARNINGLOG = f"{self.LOGDIRECTORY}/FTS_warning.log"
       self.DEBUGLOG = f"{self.LOGDIRECTORY}/FTS_debug.log"
       self.INFOLOG = f"{self.LOGDIRECTORY}/FTS_info.log"
       self.HTTPLOG = f"{self.LOGDIRECTORY}/FTS_http.log"
       self.DELIMITER = ' ? '
       self.MAXFILESIZE = 100000
       self.BACKUPCOUNT = 5
       #http server config
       self.DATABASENAME = 'TAK.db'
       path = pathlib.Path(self.DATABASENAME)
       fullPath = path.absolute()
       fullPath = fullPath.as_posix()
       self.DATABASE = fullPath
       self.HTTPPORT = '8080'
       self.DEFAULTRETURN = 'other'
       self.GET = 'GET'
       self.PUT = 'PUT'
       self.POST = 'POST'
       self.DATAPACKAGEFOLDER = 'DataPackages'
       self.versionInfo = 'FreeTAKServer-0.7.0.2-Alpha'
       self.NodeID = 'Public-FTS'
       self.VERSIONJSON = '{"version":"2","type":"ServerConfig", "data":{"version": "%s", "api": "2","hostname":"%s"}, "nodeId":"%s"}' % (self.versionInfo, self.IP ,self.NodeID)
       self.HTTPDEBUG = False
       self.HTTPMETHODS = ['POST', 'GET', 'PUT']
