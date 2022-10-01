from .RoutingProxyServiceVariables import RoutingProxyServiceVariables as vars


class RoutingProxyService:
    def __init__(
        self,
        RoutingProxySubscriberPort: int = vars().RoutingProxySubscriberPort,
        RoutingProxySubscriberIP: str = vars().RoutingProxySubscriberIP,
        RoutingProxySubscriberProtocol: str = vars().RoutingProxySubscriberProtocol,
        RoutingProxyPublisherPort: int = vars().RoutingProxyPublisherPort,
        RoutingProxyPublisherIP: str = vars().RoutingProxyPublisherIP,
        RoutingProxyPublisherProtocol: str = vars().RoutingProxyPublisherProtocol,
        RoutingProxyRequestServerPort: int = vars().RoutingProxyRequestServerPort,
        RoutingProxyRequestServerIP: str = vars().RoutingProxyRequestServerIP,
        RoutingProxyRequestServerProtocol: str = vars().RoutingProxyRequestServerProtocol,
        RoutingProxyServiceStatus: str = vars().RoutingProxyServiceStatus,
        NumRoutingWorkers: str = vars().NumRoutingWorkers,
    ):
        self.RoutingProxySubscriberPort = RoutingProxySubscriberPort
        self.RoutingProxySubscriberIP = RoutingProxySubscriberIP
        self.RoutingProxySubscriberProtocol = RoutingProxySubscriberProtocol
        self.RoutingProxyPublisherPort = RoutingProxyPublisherPort
        self.RoutingProxyPublisherIP = RoutingProxyPublisherIP
        self.RoutingProxyPublisherProtocol = RoutingProxyPublisherProtocol
        self.RoutingProxyRequestServerPort = RoutingProxyRequestServerPort
        self.RoutingProxyRequestServerIP = RoutingProxyRequestServerIP
        self.RoutingProxyRequestServerProtocol = RoutingProxyRequestServerProtocol
        self.RoutingProxyServiceStatus = RoutingProxyServiceStatus
        self.NumRoutingWorkers = NumRoutingWorkers
