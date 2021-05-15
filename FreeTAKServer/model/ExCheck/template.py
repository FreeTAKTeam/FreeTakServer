from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

class template:
    def __init__(self):
        self.version = "2"
        self.type = "Mission"
        self.data = []
        self.nodeId = MainConfig.nodeID