from FreeTAKServer.model.ServiceObjects.SSLDataPackageVariables import SSLDataPackageVariables as vars
class SSLDataPackageService:
    def __init__(self, SSLDataPackageServiceIP = vars().SSLDataPackageIP,
                 SSLDataPackageServicePort = vars().SSLDataPackagePort,
                 SSLDataPackageServiceStatus = vars().SSLDataPackageStatus):
        self.SSLDataPackageServiceIP = SSLDataPackageServiceIP
        self.SSLDataPackageServicePort = SSLDataPackageServicePort
        self.SSLDataPackageServiceStatus = SSLDataPackageServiceStatus