from FreeTAKServer.controllers.configuration.MainConfig import MainConfig


class RoutingProxyServiceVariables:
    def __init__(self):
        self.RoutingProxySubscriberPort = MainConfig.RoutingProxySubscriberPort
        self.RoutingProxySubscriberIP = MainConfig.RoutingProxySubscriberIP
        self.RoutingProxySubscriberProtocol = "tcp"
        self.RoutingProxyPublisherPort = MainConfig.RoutingProxyPublisherPort
        self.RoutingProxyPublisherIP = MainConfig.RoutingProxyPublisherIP
        self.RoutingProxyPublisherProtocol = "tcp"
        self.RoutingProxyRequestServerPort = MainConfig.RoutingProxyRequestServerPort
        self.RoutingProxyRequestServerIP = MainConfig.RoutingProxyRequestServerIP
        self.RoutingProxyRequestServerProtocol = "tcp"
        self.NumRoutingWorkers = MainConfig.NumRoutingWorkers
        self.RoutingProxyServiceStatus = ""
