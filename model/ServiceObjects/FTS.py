from .FTSVariables import FTSVariables as vars
from .CoTService import CoTService
from .TCPDataPackageService import TCPDataPackageService
from .SSLDataPackageService import SSLDataPackageService
from .RestAPIService import RestAPIService
from .SSLCoTService import SSLCoTService
from .FederationClientService import FederationClientService
from .FederationServerService import FederationServerService

class FTS:
    def __init__(self):
        self.CoTService = CoTService()
        self.TCPDataPackageService = TCPDataPackageService()
        self.SSLDataPackageService = SSLDataPackageService()
        self.RestAPIService = RestAPIService()
        self.SSLCoTService = SSLCoTService()
        self.FederationClientService = FederationClientService()
        self.FederationServerService = FederationServerService()