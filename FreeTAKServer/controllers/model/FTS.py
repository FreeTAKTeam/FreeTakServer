from .FTSVariables import FTSVariables as vars
from .CoTService import CoTService
from .DataPackageService import DataPackageService
from .RestAPIService import RestAPIService

class FTS:
    def __init__(self):
        self.CoTService = CoTService()
        self.DataPackageService = DataPackageService()
        self.RestAPIService = RestAPIService()
        