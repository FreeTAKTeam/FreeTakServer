class LoggingConstants:
    def __init__(self):
        #main logging config
        self.LOGFORMAT = '%(levelname)s : %(asctime)s : %(filename)s:%(lineno)d : %(message)s'
        self.LOGNAME = 'FTS'
        self.LOGDIRECTORY = 'logs'
        self.WARNINGLOG = f"{self.LOGDIRECTORY}/{self.LOGNAME}_warning.log"
        self.DEBUGLOG = f"{self.LOGDIRECTORY}/{self.LOGNAME}_debug.log"
        self.INFOLOG = f"{self.LOGDIRECTORY}/{self.LOGNAME}_info.log"
        self.HTTPLOG = f"{self.LOGDIRECTORY}/{self.LOGNAME}_http.log"
        self.DELIMITER = ' ? '
        self.MAXFILESIZE = 100000
        self.BACKUPCOUNT = 5