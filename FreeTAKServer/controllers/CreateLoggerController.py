from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from logging.handlers import RotatingFileHandler
import logging
import sys
import os
loggingConstants = LoggingConstants()
class CreateLoggerController:
    def __init__(self, loggername):
        self.currentpath = os.path.dirname(os.path.realpath(__file__))
        self.logger = logging.getLogger(loggername)
        self.logger.propagate = True
        log_format = logging.Formatter(loggingConstants.LOGFORMAT)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.newHandler(loggingConstants.DEBUGLOG, logging.DEBUG, log_format))
        self.logger.addHandler(self.newHandler(loggingConstants.WARNINGLOG, logging.WARNING, log_format))
        self.logger.addHandler(self.newHandler(loggingConstants.INFOLOG, logging.INFO, log_format))
        """console = logging.StreamHandler(sys.stdout)
        console.setFormatter(log_format)
        console.setLevel(logging.DEBUG)
        self.logger.info('test')
        self.logger.addHandler(console)"""

    def newHandler(self, filename, log_level, log_format):
        handler = RotatingFileHandler(
            filename,
            maxBytes=loggingConstants.MAXFILESIZE,
            backupCount=loggingConstants.BACKUPCOUNT
        )
        handler.setFormatter(log_format)
        handler.setLevel(log_level)
        return handler

    def getLogger(self):
        return self.logger