from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()

class IntegrationManagerServiceVariables:
    def __init__(self) -> None:
        self.IntegrationManagerPullerProtocol = "tcp"
        self.IntegrationManagerPullerAddress = config.IntegrationManagerPullerAddress
        self.IntegrationManagerPullerPort = config.IntegrationManagerPullerPort
        self.IntegrationManagerPublisherProtocol = "tcp"
        self.IntegrationManagerPublisherAddress = config.IntegrationManagerPublisherAddress
        self.IntegrationManagerPublisherPort = config.IntegrationManagerPublisherPort