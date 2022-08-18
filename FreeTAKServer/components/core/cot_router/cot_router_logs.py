import logging
import logging.config
from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from .cot_router_constants import LOGGING_CONFIGURATION_PATH

class COTRouterLogs(Controller):
    def __init__(self):
        logging.config.fileConfig(LOGGING_CONFIGURATION_PATH)
        self.logger = logging.getLogger('cot_router')
    
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def get_logger(self):
        """get the logger for the cot_router component.
        
        Returns:
            logging.Logger: a logger object for the emergency component.
        """
        return self.logger
    
    def get_logs(self, **kwargs):
        self.response.set_values(kwargs)
        with open(self.logger.handlers[0].baseFilename, 'r') as f:
            return f.read()