from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()


class RoutingProxyServiceVariables:
    def __init__(self):
        self.RoutingProxySubscriberPort = config.RoutingProxySubscriberPort
        self.RoutingProxySubscriberIP = config.RoutingProxySubscriberIP
        self.RoutingProxySubscriberProtocol = "tcp"
        self.RoutingProxyPublisherPort = config.RoutingProxyPublisherPort
        self.RoutingProxyPublisherIP = config.RoutingProxyPublisherIP
        self.RoutingProxyPublisherProtocol = "tcp"
        self.RoutingProxyRequestServerPort = config.RoutingProxyRequestServerPort
        self.RoutingProxyRequestServerIP = config.RoutingProxyRequestServerIP
        self.RoutingProxyRequestServerProtocol = "tcp"
        self.NumRoutingWorkers = config.NumRoutingWorkers
        self.RoutingProxyServiceStatus = ""
