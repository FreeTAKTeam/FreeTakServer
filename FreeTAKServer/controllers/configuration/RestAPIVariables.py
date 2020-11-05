class RestAPIVariables:

    defaultGeoObjectTimeout = 300
    defaultPresenceType = "a-f-G-U-C-I"

    def __init__(self):
        pass

    def function_names(self):
        self.Status = 'start_all'
        self.Clients = 'show_users'
        self.checkStatus = 'check_server_status'

    def json_vars(self):
        self.COTSERVICE = 'CoTService'
        self.DATAPACKAGESERVICE = 'TCPDataPackageService'
        self.IP = 'IP'
        self.PORT = 'PORT'
        self.STATUS = 'STATUS'

    def rest_methods(self):
        self.POST = 'POST'
        self.GET = 'GET'
        self.DELETE = 'DELETE'

    def default_values(self):
        self.defaultIP = "127.0.0.1"
        self.defaultPort = 80
        self.defaultCoTIP = '0.0.0.0'
        self.defaultCoTPort = 15777
        self.defaultCoTStatus = 'start'
        self.defaultDataPackageIP = '0.0.0.0'
        self.defaultDataPackagePort = 8080
        self.defaultDataPackageStatus = 'start'

    def json_content(self):
        self.JsonStatusStartAll = {"CoTService":
                                   {"IP": self.getdefaultCoTIP(), "PORT": self.getdefaultCoTPort(), "STATUS": self.getdefaultCoTStatus()},
                               "TCPDataPackageService":
                                   {"IP": self.getdefaultDataPackageIP(), "PORT": self.getdefaultDataPackagePort(), "STATUS": self.getdefaultDataPackageStatus()}}

        self.JsonStatusStopAll = {"CoTService":
                                      {"STATUS": "stop"},
                                  "TCPDataPackageService":
                                      {"STATUS": "stop"}}
        self.JsonStatusStartCoTService = {}

    def setJsonStatusStartAll(self, JsonStatusStartAll):
        self.JsonStatusStartAll = JsonStatusStartAll

    def getJsonStatusStartAll(self):
        self.json_content()
        return self.JsonStatusStartAll

    def setdefaultCoTIP(self, defaultCoTIP):
        self.defaultCoTIP = defaultCoTIP

    def getdefaultCoTIP(self):
        return self.defaultCoTIP

    def setdefaultCoTPort(self, defaultCoTPort):
        self.defaultCoTPort = defaultCoTPort

    def getdefaultCoTPort(self):
        return self.defaultCoTPort

    def setdefaultCoTStatus(self, defaultCoTStatus):
        self.defaultCoTStatus = defaultCoTStatus

    def getdefaultCoTStatus(self):
        return self.defaultCoTStatus

    def setdefaultDataPackageIP(self, defaultDataPackageIP):
        self.defaultDataPackageIP = defaultDataPackageIP

    def getdefaultDataPackageIP(self):
        return self.defaultDataPackageIP

    def setdefaultDataPackagePort(self, defaultDataPackagePort):
        self.defaultDataPackagePort = defaultDataPackagePort

    def getdefaultDataPackagePort(self):
        return self.defaultDataPackagePort
    
    def setdefaultDataPackageStatus(self, defaultDataPackageStatus):
        self.defaultDataPackageStatus = defaultDataPackageStatus

    def getdefaultDataPackageStatus(self):
        return self.defaultDataPackageStatus