from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from logging.handlers import RotatingFileHandler
import logging
import os
import sys
loggingConstants = LoggingConstants()
class CreateLoggerController:
    def __init__(self, loggername, logging_constants = loggingConstants):
        self.logger = logging.getLogger(loggername)
        self.logger.propagate = True
        log_format = logging.Formatter(logging_constants.LOGFORMAT)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.newHandler(logging_constants.DEBUGLOG, logging.DEBUG, log_format, logging_constants))
        self.logger.addHandler(self.newHandler(logging_constants.ERRORLOG, logging.ERROR, log_format, logging_constants))
        self.logger.addHandler(self.newHandler(logging_constants.INFOLOG, logging.INFO, log_format, logging_constants))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        """console = logging.StreamHandler(sys.stdout)
        console.setFormatter(log_format)
        console.setLevel(logging.DEBUG)
        self.logger.info('test')
        self.logger.addHandler(console)"""

    def newHandler(self, filename, log_level, log_format, logging_constants):
        handler = RotatingFileHandler(
            filename,
            maxBytes=logging_constants.MAXFILESIZE,
            backupCount=logging_constants.BACKUPCOUNT
        )
        handler.setFormatter(log_format)
        handler.setLevel(log_level)
        return handler

    def getLogger(self):
        return self.logger