from FreeTAKServer.components.core.abstract_component.facade import Facade
from . import domain
from FreeTAKServer.components.core.cot_router.cot_router_constants import CONFIGURATION_PATH_TEMPLATE, ACTION_MAPPING_PATH
from FreeTAKServer.components.core.cot_router.cot_router_main import COTRouter
from FreeTAKServer.components.core.cot_router.cot_router_logs import COTRouterLogs

class COTRouterFacade(Facade):
    
    state = None
    
    def __init__(self):
        # this if statement insures that COTRouterFacade is a singleton
        # this prevents reloading of the domain and other wasteful operations
        if self.state is None:
            self.cot_router = COTRouter()
            self.cot_router_logs = COTRouterLogs()
            super().__init__(CONFIGURATION_PATH_TEMPLATE, domain, ACTION_MAPPING_PATH, self.cot_router_logs)
            COTRouterFacade.state = self.__dict__
        else:
            self.__dict__ = COTRouterFacade.state
    
    def initialize(self, request, response):
        self.cot_router.initialize(request, response)
        return super().initialize(request, response)
    
    def get_logs(self):
        self.cot_router_logs.get_logs(**self.request.get_values())
    
    def cot_received(self):
        self.cot_router.cot_received(**self.request.get_values())
        
    def cot_broadcast(self):
        self.cot_router.cot_broadcast(**self.request.get_values())