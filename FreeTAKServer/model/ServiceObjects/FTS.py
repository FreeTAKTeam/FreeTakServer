from .CoTService import CoTService
from .FederationClientService import FederationClientService
from .FederationServerService import FederationServerService
from .FTSVariables import FTSVariables as vars
from .RestAPIService import RestAPIService
from .RoutingProxyService import RoutingProxyService
from .SSLCoTService import SSLCoTService
from .SSLDataPackageService import SSLDataPackageService
from .TCPDataPackageService import TCPDataPackageService
from .ComponentRegistration import ComponentRegistration


class FTS:
    def __init__(self):
        self.CoTService = CoTService()
        self.TCPDataPackageService = TCPDataPackageService()
        self.SSLDataPackageService = SSLDataPackageService()
        self.RestAPIService = RestAPIService()
        self.SSLCoTService = SSLCoTService()
        self.FederationClientService = FederationClientService()
        self.FederationServerService = FederationServerService()
        self.RoutingProxyService = RoutingProxyService()
        self.ComponentRegistration = ComponentRegistration()
