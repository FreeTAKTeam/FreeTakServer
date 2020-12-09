from .DataPackageServiceVariables import DataPackageServiceVariables as vars

class DataPackageService:
    def __init__(self, DataPackageServiceIP = vars().DataPackageServiceIP, 
                 DataPackageServicePort = vars().DataPackageServicePort, 
                 DataPackageServiceStatus = vars().DataPackageServiceStatus):
        self.DataPackageServiceIP = DataPackageServiceIP
        self.DataPackageServicePort = DataPackageServicePort
        self.DataPackageServiceStatus = DataPackageServiceStatus