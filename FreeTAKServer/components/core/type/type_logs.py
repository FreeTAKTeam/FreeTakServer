import logging
import logging.config
from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response

from .type_constants import LOGGING_CONFIGURATION_PATH

class TypeLogs(Controller):
    
    def __init__(self):
        logging.config.fileConfig(LOGGING_CONFIGURATION_PATH)
        self.logger = logging.getLogger('type')

    def accept_visitor(self, visitor):
        pass
    
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def get_logger(self, **kwargs):
        """get the logger for the type component.
        
        Returns:
            logging.Logger: a logger object for the type component.
        """
        return self.logger
    
    def get_logs(self, **kwargs):
        self.response.set_values(kwargs)
        
        with open(self.logger.handlers[0].baseFilename, 'r') as f:
            return f.read()