from .IntegrationManagerServiceVariables import IntegrationManagerServiceVariables as vars

class IntegrationManagerService:
    def __init__(self, IntegrationManagerPullerProtocol: str = vars().IntegrationManagerPullerProtocol, IntegrationManagerPullerAddress: str = vars().IntegrationManagerPullerAddress, IntegrationManagerPullerPort: int = vars().IntegrationManagerPullerPort,
    IntegrationManagerPublisherProtocol: str = vars().IntegrationManagerPublisherProtocol, IntegrationManagerPublisherAddress: str = vars().IntegrationManagerPublisherAddress, IntegrationManagerPublisherPort = vars().IntegrationManagerPublisherPort) -> None:
        self.IntegrationManagerPullerProtocol = IntegrationManagerPullerProtocol
        self.IntegrationManagerPullerAddress = IntegrationManagerPullerAddress
        self.IntegrationManagerPullerPort = IntegrationManagerPullerPort
        self.IntegrationManagerPublisherProtocol = IntegrationManagerPublisherProtocol
        self.IntegrationManagerPublisherAddress = IntegrationManagerPublisherAddress
        self.IntegrationManagerPublisherPort = IntegrationManagerPublisherPort