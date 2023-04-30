from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from logging.handlers import RotatingFileHandler
import logging
import os
import sys

config = MainConfig.instance()

loggingConstants = LoggingConstants()
class CreateLoggerController:
    def __init__(self, loggername, logging_constants=loggingConstants):
        self.logger = logging.getLogger(loggername)
        self.logger.propagate = True
        log_format = logging.Formatter(logging_constants.LOGFORMAT)

        if config.LogLevel.lower() == "info":
            log_level = logging.INFO
            self.logger.addHandler(self.newHandler(logging_constants.INFOLOG, log_level, log_format, logging_constants))
        elif config.LogLevel.lower() == "error":
            log_level = logging.ERROR
            self.logger.addHandler(self.newHandler(logging_constants.ERRORLOG, log_level, log_format, logging_constants))
        elif config.LogLevel.lower() == "debug":
            log_level = logging.DEBUG
            self.logger.addHandler(self.newHandler(logging_constants.DEBUGLOG, log_level, log_format, logging_constants))
            

        self.logger.setLevel(log_level)
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
