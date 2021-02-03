class RestAPIVariables:

    defaultGeoObjectTimeout = 300
    defaultPresenceTimeout = 500
    defaultPresenceType = "a-f-G-U-C-I"

    def __init__(self):
        pass

    def function_names(self):
        self.Status = 'start_all'
        self.Clients = 'show_users'
        self.checkStatus = 'check_server_status'

    def json_vars(self):
        self.COTSERVICE = 'TCP_CoT_service'
        self.DATAPACKAGESERVICE = 'TCP_DataPackage_service'
        self.SSLCOTSERVICE = 'SSL_CoT_service'
        self.SSLDATAPACKAGESERVICE = 'SSL_DataPackage_service'
        self.FEDERATIONCLIENTSERVICE = 'Federation_Client_service'
        self.FEDERATIONSERVERSERVICE = 'Federation_server_service'
        self.RESTAPISERVICE = 'Rest_API_service'
        self.IP = 'ip'
        self.PORT = 'port'
        self.STATUS = 'status'

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
        self.defaultSSLCoTIP = '0.0.0.0'
        self.defaultSSLCoTPort = 15778
        self.defaultSSLCoTStatus = 'start'
        self.defaultFederationClientIP = '0.0.0.0'
        self.defaultFederationClientPort = 9000
        self.defaultFederationClientStatus = ''
        self.defaultFederationServerIP = '0.0.0.0'
        self.defaultFederationServerPort = 9000
        self.defaultFederationServerStatus = ''

    def json_content(self):
        self.JsonStatusStartAll = {"CoTService":
                                   {"IP": self.getdefaultCoTIP(), "PORT": self.getdefaultCoTPort(), "STATUS": self.getdefaultCoTStatus()},
                                   "TCPDataPackageService":
                                   {"IP": self.getdefaultDataPackageIP(), "PORT": self.getdefaultDataPackagePort(), "STATUS": self.getdefaultDataPackageStatus()},
                                   "SSLCoTService":
                                       {"IP": self.getdefaultSSLCoTIP(), "PORT": self.getdefaultSSLCoTPort(), "STATUS": self.getdefaultSSLCoTStatus()},
                                   "FederationClientService":
                                       {"IP": self.getdefaultFederationClientIP(), "PORT": self.getdefaultFederationClientPort(), "STATUS": self.getdefaultFederationClientStatus()},
                                   "FederationServerService":
                                       {"IP": self.getdefaultFederationServerIP(), "PORT": self.getdefaultFederationServerPort(), "STATUS": self.getdefaultFederationServerStatus()}}
        self.JsonStatusStopAll = {"CoTService":
                                  {"STATUS": "stop"},
                                  "TCPDataPackageService":
                                      {"STATUS": "stop"},
                                  "SSLCoTService":
                                      {"STATUS": "stop"},
                                  "FederationClientService":
                                      {"STATUS": "stop"},
                                  "FederationServerService":
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

    def setdefaultSSLCoTPort(self, defaultSSLCoTPort):
        self.defaultSSLCoTPort = defaultSSLCoTPort

    def getdefaultSSLCoTPort(self):
        return self.defaultSSLCoTPort

    def setdefaultSSLCoTIP(self, defaultSSLCoTIP):
        self.defaultSSLCoTIP = defaultSSLCoTIP

    def getdefaultSSLCoTIP(self):
        return self.defaultSSLCoTIP

    def setdefaultSSLCoTStatus(self, defaultSSLCoTStatus):
        self.defaultSSLCoTStatus = defaultSSLCoTStatus

    def getdefaultSSLCoTStatus(self):
        return self.defaultSSLCoTStatus

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

    def setdefaultFederationClientIP(self, defaultFederationClientIP):
        self.defaultFederationClientIP = defaultFederationClientIP

    def getdefaultFederationClientIP(self):
        return self.defaultFederationClientIP

    def setdefaultFederationClientPort(self, defaultFederationClientPort):
        self.defaultFederationClientPort = defaultFederationClientPort

    def getdefaultFederationClientPort(self):
        return self.defaultFederationClientPort

    def setdefaultFederationClientStatus(self, defaultFederationClientStatus):
        self.defaultFederationClientStatus = defaultFederationClientStatus

    def getdefaultFederationClientStatus(self):
        return self.defaultFederationClientStatus

    def setdefaultFederationServerIP(self, defaultFederationServerIP):
        self.defaultFederationServerIP = defaultFederationServerIP

    def getdefaultFederationServerIP(self):
        return self.defaultFederationServerIP

    def setdefaultFederationServerPort(self, defaultFederationServerPort):
        self.defaultFederationServerPort = defaultFederationServerPort

    def getdefaultFederationServerPort(self):
        return self.defaultFederationServerPort

    def setdefaultFederationServerStatus(self, defaultFederationServerStatus):
        self.defaultFederationServerStatus = defaultFederationServerStatus

    def getdefaultFederationServerStatus(self):
        return self.defaultFederationServerStatus
