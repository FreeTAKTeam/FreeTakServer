from FreeTAKServer.model.RawConnectionInformation import RawConnectionInformation

class RawSSLConnectionInformation(RawConnectionInformation):
    def __init__(self):
        super().__init__()
        self.unwrapped_sock = None