from .FTSVariables import FTSVariables as vars
from .CoTService import CoTService
from .TCPDataPackageService import TCPDataPackageService
from .RestAPIService import RestAPIService

class FTS:
    def __init__(self):
        self.CoTService = CoTService()
        self.TCPDataPackageService = TCPDataPackageService()
        self.RestAPIService = RestAPIService()