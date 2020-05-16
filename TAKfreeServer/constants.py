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
       #Default tcp port change to change the port your FTS is listening on
       self.DEFAULTPORT = 8087
       self.LOGFILEPATH = 'log.log'
       #The buffer to receive the clients initial connection data
       self.STARTBUFFER = 32784
       #The default buffer to dynamically recieve data from client
       self.BUFFER =8192
       #The delay in seconds between the server sending data to each individual client
       #highly recomended to keep at at least 1
       #though theoretically you could make it lower but it's not advisable as with a lot of clients it may take up a lot of resources
       self.DELAY = 5
       #your current ip
       self.IP = 'Your IP'
       #Delay for the bandaid in server.py
       self.RENEWTIME = 1
       #logging config
       self.LOGTIMEFORMAT = '%(levelname)s:%(asctime)s:%(message)s:%(lineno)d'
       #the name of the log
       self.LOGNAME = 'FTS'
       #name of warning log file
       self.WARNINGLOG = 'FTS_warning.log'
       #name of debug log file
       self.DEBUGLOG = 'FTS_debug.log'
       #name of info log file
       self.INFOLOG = 'FTS_info.log'
       #delimiter between connection data DO NOT TOUCH
       self.DELIMITER = ' ? '
       #maximum size of each log file before it get deleted
       self.MAXFILESIZE = 100000
       self.BACKUPCOUNT = 5
       #http server config
       self.DATABASENAME = 'TAK.db'
       path = pathlib.Path(self.DATABASENAME)
       fullPath = path.absolute()
       fullPath = fullPath.as_posix()
       self.DATABASE = fullPath
       #the port used by the HTTP server, if you change it you must change also in your ATAK client
       self.HTTPPORT = '8080'
       self.DEFAULTRETURN = 'other'
       self.GET = 'GET'
       self.PUT = 'PUT'
       self.POST = 'POST'
       self.DATAPACKAGEFOLDER = 'DataPackages'
       #DO NO TOUCH IF YOU WANT SUPPORT!!!  
       self.versionInfo = 'FreeTAKServer-0.7.0.2-Alpha'
       # Optional Name of your server  
       self.NodeID = 'Mighty Parrot'
       self.VERSIONJSON = '{"version":"2","type":"ServerConfig", "data":{"version": "%s", "api": "2","hostname":"%s"}, "nodeId":"%s"}' % (self.versionInfo, self.IP ,self.NodeID)
       self.HTTPDEBUG = False
       self.HTTPMETHODS = ['POST', 'GET', 'PUT']
