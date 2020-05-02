class vars():
   def __init__(self):
       #tcp server config
       self.PING = 'ping'
       self.GEOCHAT = 'GeoChat'
       self.FAIL = 'fail'
       self.EMPTY_BYTE = b''
       self.DEFAULTPORT = 8087
       self.LOGFILEPATH = 'log.log'
       self.STARTBUFFER = 32784
       self.BUFFER =227
       self.DELAY = 5
       self.IP = '192.168.2.47'
       self.RENEWTIME = 10
       #logging config
       self.LOGTIMEFORMAT = '%(levelname)s:%(asctime)s:%(message)s'
       self.LOGNAME = 'FTS'
       self.WARNINGLOG = 'FTS_warning.log'
       self.DEBUGLOG = 'FTS_debug.log'
       self.INFOLOG = 'FTS_info.log'
       self.DELIMITER = ' ? '
       self.MAXFILESIZE = 2000000
       self.BACKUPCOUNT = 5
       #http server config
       self.DATABASE = 'TAK.db'
       self.HTTPPORT = '8080'
       self.DEFAULTRETURN = 'other'
       self.GET = 'GET'
       self.PUT = 'PUT'
       self.POST = 'POST'
       self.DATAPACKAGEFOLDER = 'DataPackages'
       self.versionInfo = 'TAK Server 1.3.12-RELEASE-2'
       self.HTTPDEBUG = False
       self.HTTPMETHODS = ['POST', 'GET', 'PUT']