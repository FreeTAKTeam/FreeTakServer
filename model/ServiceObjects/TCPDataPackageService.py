from .TCPDataPackageServiceVariables import TCPDataPackageServiceVariables as vars

class TCPDataPackageService:
    def __init__(self, TCPDataPackageServiceIP = vars().TCPDataPackageServiceIP,
                 TCPDataPackageServicePort = vars().TCPDataPackageServicePort,
                 TCPDataPackageServiceStatus = vars().TCPDataPackageServiceStatus):
        self.TCPDataPackageServiceIP = TCPDataPackageServiceIP
        self.TCPDataPackageServicePort = TCPDataPackageServicePort
        self.TCPDataPackageServiceStatus = TCPDataPackageServiceStatus