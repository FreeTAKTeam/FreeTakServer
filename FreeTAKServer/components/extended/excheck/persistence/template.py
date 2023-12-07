from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()
class template:
    def __init__(self):
        self.version = "2"
        self.type = "Mission"
        self.data = []
        self.nodeId = config.nodeID